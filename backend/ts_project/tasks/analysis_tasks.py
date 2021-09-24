from celery import shared_task
import pandas as pd
from datetime import datetime, timezone
import traceback
# import cProfile, pstats, io
from ..models import Analysis, PeriodicAnalysis, Results, Incident, Client
from ..elastic import series_search
from ..salib.model.series import Series
from ..salib.model.analyzer import Analyzer
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory
from ..adapters import SalibModelAdapter

search = series_search.SeriesSearch()

def run_analysis(client_name, data_options, model, interval):
    salib_model = SalibModelAdapter.toSalib(model)
    pipeline = Pipeline.from_json(salib_model)
    analyzer = Analyzer(pipeline=pipeline, debug=True)
    salib_inputs = {}
    client = Client.objects.get(name=client_name)
    for index, input_data in enumerate(data_options): 
        data_series = search.get_series( 
            indexname=client.index_name, 
            start=input_data.get('start', ''),  
            end=input_data.get('end', ''),  
            context=input_data.get('contexts'), 
            tags=input_data.get('tags'),             
            interval=interval,
            filter_tags=input_data.get('filterTags', False),
            filter_contexts=input_data.get('filterContexts', False),
            UTC_offset=client.utc_offset)
        dates = [datetime.fromtimestamp(item[0]/1000) for item in data_series]
        count  = [item[1] for item in data_series]
        ts = pd.Series(count, index=dates)
        #input id is just the order in the array
        salib_inputs[str(index+1)] = Series(ts)

    return  analyzer.analyze(salib_inputs)

@shared_task(bind=True)
def perform_live_analysis(self, data):
    # pr = cProfile.Profile()
    # pr.enable()
    try:        
        analysis_results = run_analysis(data['client'], data['data_options'], data['model'], data['interval'])
        output_json = analysis_results.output_format()
    except Exception as e:
        stack = traceback.format_exc()
        output_json = {
            'error': traceback.format_exc()
        }
    # pr.disable()
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
    return output_json



def update_incidents(old_incidents, new_incidents):
    from collections import OrderedDict
    new_incidents_map = OrderedDict((x['start'], x) for x in new_incidents)
    for old_inc in old_incidents:
        new_inc = new_incidents_map.get(old_inc.start, None)
        if new_inc:
            new_inc['state'] = old_inc.state
    return list(new_incidents_map.values())


@shared_task(bind=True, name="periodic_analysis")
def perform_periodic_analysis(self, id):
    periodic_analysis = PeriodicAnalysis.objects.get(id=id)
    analysis = periodic_analysis.analysis


    #override start and end dates
    now = datetime.now(timezone.utc)
    for input_data in analysis.data_options:
        input_data['start'] = ''
        input_data['end'] = now.isoformat()[:-9] + 'Z'     

    analysis_results = run_analysis(analysis.client.name, analysis.data_options, 
        analysis.model, analysis.interval).output_format()

    periodic_analysis.last_run = now 
    periodic_analysis.save()

    #save results
   # results = Results.objects.update_or_create(
   #     periodic_analysis=periodic_analysis, 
   #     defaults={
   #         'periodic_analysis': periodic_analysis,
   #         'anomalies': analysis_results['anomalies'],
   #         'run_datetime': now})

    #update incidents
    old_incidents = Incident.objects.filter(periodic_analysis=periodic_analysis)
    new_incidents = [{
        'periodic_analysis': periodic_analysis,
        'client': periodic_analysis.analysis.client.name,
        'start': datetime.fromtimestamp(anomaly['from']/1000.0, tz=timezone.utc),
        'end': datetime.fromtimestamp(anomaly['to']/1000.0, tz=timezone.utc),
        'state': Incident.State.OPEN,
        'score': anomaly.get('score', 0),
        'desc': anomaly.get('desc', '')
    } for anomaly in analysis_results['anomalies']]

    updated_incidents = update_incidents(old_incidents, new_incidents)
    old_incidents.delete()
    for incident_data in updated_incidents:
        Incident.objects.create(**incident_data) 
from celery import shared_task
from ..models import PeriodicAnalysis, Results, Incident

import pandas as pd
from datetime import datetime, timezone
from .. import services
from ..salib.model.series import Series
from ..salib.model.analyzer import Analyzer
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory
from ..adapters import SalibModelAdapter

import cProfile, pstats, io
import json

def run_analysis(client, inputs_data, model):
    salib_model = SalibModelAdapter.toSalib(model)
    pipeline = Pipeline.from_json(salib_model)
    analyzer = Analyzer(pipeline=pipeline, debug=True)

    salib_inputs = {}
    for index, input_data in enumerate(inputs_data): 
        data_series = services.get_series( 
            client_name=client, 
            contexts=input_data.get('contexts', []), 
            start=input_data.get('start', ''),  
            end=input_data.get('end', ''),  
            tags=input_data.get('tags', []),             
            interval=input_data.get('interval', '1h'))
        dates = [datetime.fromtimestamp(item[0]/1000) for item in data_series]
        count  = [item[1] for item in data_series]
        ts = pd.Series(count, index=dates)
        #input id is just the order in the array
        salib_inputs[str(index+1)] = Series(ts)

    return  analyzer.analyze(salib_inputs)


@shared_task(bind=True)
def perform_live_analysis(self, data):
    pr = cProfile.Profile()
    pr.enable()
    analysis_results = run_analysis(data['client'], data['data_options'], data['model'])
    output_json = analysis_results.output_format()
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    return output_json


@shared_task(bind=True, name="periodic_analysis")
def perform_periodic_analysis(self, id):
    periodic_analysis = PeriodicAnalysis.objects.get(id=id)
    analysis_settings = periodic_analysis.analysis

    inputs_data = analysis_settings.data_options
    now = datetime.now(timezone.utc)

    #override start and end dates
    for input_data in inputs_data:
        input_data['start'] = ''
        input_data['end'] = now.isoformat()[:-9] + 'Z'     

    print('''Running analysis with ID:  {analysis_id}, interval {interval} and relevant period {relevant}'''.format(
        analysis_id=periodic_analysis.analysis_id, 
        interval=periodic_analysis.time_interval, 
        relevant=periodic_analysis.relevant_period))

    analysis_results = run_analysis(analysis_settings.client, inputs_data, analysis_settings.model).output_format()

    periodic_analysis.last_run = now 
    periodic_analysis.save()

    #save results
    results = Results.objects.create(
        periodic_analysis=periodic_analysis, 
        anomalies=analysis_results['anomalies'],
        run_datetime=now)

    #create incidents (remove old for now)
    Incident.objects.filter(periodic_analysis=periodic_analysis).delete()
    for anomaly in analysis_results['anomalies']:
        incident = Incident.objects.create(
            periodic_analysis=periodic_analysis,
            client=periodic_analysis.analysis.client.name,
            start=datetime.fromtimestamp(anomaly['from']/1000.0, tz=timezone.utc),
            end=datetime.fromtimestamp(anomaly['to']/1000.0, tz=timezone.utc),
            score=anomaly['score'],
            desc=anomaly['desc'])


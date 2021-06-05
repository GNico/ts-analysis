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


def run_analysis(data, model):
    salib_model = SalibModelAdapter.toSalib(model)
    pipeline = Pipeline.from_json(salib_model)
    analyzer = Analyzer(pipeline=pipeline, debug=True)

    data_series = services.get_series( 
        client_name=data.get('client', ''), 
        contexts=data.get('contexts', []), 
        start=data.get('start', ''),  
        end=data.get('end', ''),  
        tags=data.get('tags', []),             
        interval=data.get('interval', '1h'))
    dates = [pd.to_datetime(item[0], unit="ms") for item in data_series]
    count  = [item[1] for item in data_series]
    ts = pd.Series(count, index=dates)
    series = Series(ts)

    # TODO
    # inputs = {
    #    "input_id" : Series
    # }

    return  analyzer.analyze(inputs)


@shared_task(bind=True)
def perform_live_analysis(self, data):
    analysis_results = run_analysis(data, data['model'])
    output_json = analysis_results.output_format()
    return output_json


@shared_task(bind=True, name="periodic_analysis")
def perform_periodic_analysis(self, id):
    periodic_analysis = PeriodicAnalysis.objects.get(id=id)
    analysis_settings = periodic_analysis.analysis

    data = analysis_settings.data_options
    now = datetime.now(timezone.utc)

    #force end of data to current datetime
    data['start'] = ''
    data['end'] = now.isoformat()[:-9] + 'Z' 

    print('''Running analysis with ID:  {analysis_id}, interval {interval} and relevant period {relevant}'''.format(
        analysis_id=periodic_analysis.analysis_id, 
        interval=periodic_analysis.time_interval, 
        relevant=periodic_analysis.relevant_period))

    analysis_results = run_analysis(data, analysis_settings.model).output_format()

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
            start=datetime.fromtimestamp(anomaly['from']/1000.0, tz=timezone.utc),
            end=datetime.fromtimestamp(anomaly['to']/1000.0, tz=timezone.utc),
            score=anomaly['score'],
            desc=anomaly['desc']
        )


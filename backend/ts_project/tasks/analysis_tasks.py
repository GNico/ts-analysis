from celery import shared_task

import pandas as pd
from .. import services
from ..salib.model.series import Series
from ..salib.model.analyzer import Analyzer
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory

@shared_task(bind=True)
def perform_analysis(self, data):
    print(data)
    pipeline = Pipeline.from_json(data['model'])
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

    analyzer = Analyzer(pipeline=pipeline)
    analysis = analyzer.analyze(series)
    return analysis.output_format()
        

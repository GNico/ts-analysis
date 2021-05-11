from celery import shared_task

import pandas as pd
from .. import services
from ..salib.model.series import Series
from ..salib.model.analyzer import Analyzer
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory

from ..adapters import SalibModelAdapter


@shared_task(bind=True)
def perform_analysis(self, data):
    model = SalibModelAdapter.toSalib(data['model'])
    pipeline = Pipeline.from_json(model)
    analyzer = Analyzer(pipeline=pipeline)

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

    analysis = analyzer.analyze(series)
    output_json = analysis.output_format()
    return output_json

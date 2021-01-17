from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    
import pandas as pd

from ..salib.model.series import Series
from ..salib.model.analyzer import Analyzer
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory

class AnalysisView(APIView):
    def get(self, request):
        data_series = services.get_series( 
            #note: si no envia parametro usa 'movistar' default, cambiar luego para que tire error
            client_name=request.query_params.get('name', 'movistar'), 
            contexts=request.query_params.getlist('contexts', []), 
            start=request.query_params.get('start', ''),  
            end=request.query_params.get('end', ''),  
            tags=request.query_params.getlist('tags', []),             
            interval=request.query_params.get('interval', '1h'))

        dates = [pd.to_datetime(item[0], unit="ms") for item in data_series]
        count  = [item[1] for item in data_series]
        ts = pd.Series(count, index=dates)

        series = Series(ts)

        obj = {
            'nodes': [
                {
                    'id': '1',
                    'class': 'aggregator',
                    'type': 'OR',
                    'params': [],
                    'sources': ['2', '3']
                },
                {
                    'id': '2',
                    'class': 'detector',
                    'type': 'EMA',
                    'params': [
                        {
                            'id': 'decay',
                            'value': 0.95
                        },
                        {
                            'id': 'threshold',
                            'value': 1
                        }
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'class': 'detector',
                    'type': 'EMA',
                    'params': [
                        {
                            'id': 'decay',
                            'value': 0.9
                        },
                        {
                            'id': 'threshold',
                            'value': 2
                        }
                    ],
                    'sources': []
                }
            ]
        }

        pipeline = Pipeline.from_json(obj)

        builder = NodeFactory.detector('test_id', 'EMA')
        builder.set_param_value('decay', 0.95)
        builder.set_param_value('threshold', 1)
        ema = builder.build()

        analyzer = Analyzer(pipeline=pipeline, baseline_algo=ema)
        analysis = analyzer.analyze(series)
        response = analysis.output_format()
        return Response(response)



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

    def post(self, request):
        data = request.data
        # TODO: deberia pinchar con mas gracia si esta vacio
        pipeline_obj = data['model']
        # TODO: cleanup
        print("PIPELINE OBJ:", data['model'])
        pipeline = Pipeline.from_json(pipeline_obj)


        data_series = services.get_series( 
            # TODO: si no envia parametro usa 'movistar' default, cambiar luego para que tire error
            client_name=data.get('name', 'movistar'), 
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
        response = analysis.output_format()
        
        return Response(response)


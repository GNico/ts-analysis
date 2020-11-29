from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    
import pandas as pd

from ..salib.model.series import Series


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
        print("SERIES:", ts)
        series = Series(ts)
        print("INTERVAL", series.interval)

        response = {
            "series": series,
            "anomalies": anomalies, 
        }
        print("RESPONSE: ", response)
        return Response(response)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    
import pandas as pd
from adtk.data import validate_series
from adtk.detector import QuantileAD


class AnalysisView(APIView):
    def get(self, request):
        series = services.get_series( 
            client_name=request.query_params.get('name', 'movistar'),  #note: si no envia parametro usa 'movistar' default, cambiar luego para que tire error
            contexts=request.query_params.getlist('contexts', []), 
            start=request.query_params.get('start', ''),  
            end=request.query_params.get('end', ''),  
            tags=request.query_params.getlist('tags', []),             
            interval=request.query_params.get('interval', '1h'))

        dates = [pd.to_datetime(item[0], unit="ms") for item in series]
        count  = [item[1] for item in series]
        ts = pd.Series(count, index=dates)

        s = validate_series(ts)
        quantile_ad = QuantileAD(high=0.99)
        anomalies = quantile_ad.fit_detect(s, return_list=True)
        anoms = []
        for anomaly in anomalies: 
            anoms.append({
                "from": int(anomaly[0].value / 10**6),
                "to": int(anomaly[1].value / 10**6),
                "score": 50,
                })
        response = {
            "series": series,
            "anomalies": anoms, 
        }
        return Response(response)



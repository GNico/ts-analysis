from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    
from . import mock_data


class AnalysisView(APIView):
    def get(self, request):
         #mocking
        data = {
          "series": mock_data.SERIES,
          "anomalies": mock_data.ANOMALIES,
          "trend": mock_data.TREND,
          "baseline": mock_data.BASELINE
        }
        return Response(data)

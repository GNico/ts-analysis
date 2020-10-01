from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    

import os
import json


class AlgoTestView(APIView):
    def get(self, request):
      #mock
      test_file_path = os.environ.get('TEST_PATH')
      test_file_path += "/algotest.json"

      print(test_file_path)
      with open(test_file_path) as test_file:
          data = json.load(test_file)
      return Response(data)

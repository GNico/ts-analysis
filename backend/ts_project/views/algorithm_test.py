from rest_framework.response import Response
from rest_framework.views import APIView

import json
import os


class AlgoTestView(APIView):
    def get(self, request):
        source = request.GET.get('source') + ".json"
        path = os.getcwd() + "/ts_project/algo_test_output/" + source
        with open(path) as test_file:
            data = json.load(test_file)
        return Response(data)

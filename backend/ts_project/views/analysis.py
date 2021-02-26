from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import AnalysisSerializer
from .. import tasks

class AnalysisView(APIView):
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        task = tasks.perform_analysis.delay(serializer.data)
        return Response({"task_id": task.id})


class AnalysisResultView(APIView):
    def get(self, request, id): 
        task = tasks.perform_analysis.AsyncResult(id)
        if  task.state == 'PENDING' or task.state == 'PROGRESS' or task.state == 'STARTED':
            return Response({"task_id": id, "state": "pending"})
        elif task.state == 'SUCCESS':
            res = task.result
            nodes = request.query_params.getlist('nodes', [])           
            if (nodes):
                node_results = { k:getattr(res['debug_nodes'], k, {}) for k in nodes}
                return Response({"task_id": id, "state": "success", "node_results": node_results}) 
            else:
                #final_result = { 'series': res['series'], 'anomalies': res['anomalies'] }
                return Response({"task_id": id, "state": "success", "result": res})            
        elif task.state == 'FAILED':
            return Response({"task_id": id, "state": "failed", "error": "An error occurred while performing the analysis"}) 


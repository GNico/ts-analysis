from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import AnalysisSerializer
from .. import tasks
from .. import task_priorities


class AnalysisView(APIView):
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        task = tasks.perform_live_analysis.apply_async(args=[serializer.data], priority=task_priorities.LIVE_ANALYSIS)
        return Response({"task_id": task.id})


class AnalysisResultView(APIView):
    def get(self, request, id): 
        task = tasks.perform_live_analysis.AsyncResult(id)
        if  task.state == 'PENDING' or task.state == 'PROGRESS' or task.state == 'STARTED':
            return Response({"task_id": id, "state": "pending"})
        elif task.state == 'SUCCESS':
            res = task.result
            if 'error' in res:
                return Response({
                    "task_id": id,
                    "state": "failed",
                    "error": res['error']
                })
            nodes = request.query_params.getlist('nodes', [])           
            if (nodes):
                node_results = { k: res['debug_nodes'].get(k, None) for k in nodes}
                res['debug_nodes'] = node_results
                return Response({
                    'task_id': id, 
                    'state': 'success', 
                    'result': res
                }) 
            else:
                #final_result = { 'series': res['series'], 'anomalies': res['anomalies'] }
                res.pop('debug_nodes', None)
                return Response({
                    "task_id": id, 
                    "state": "success", 
                    "result": res
                })                            
        elif task.state == 'FAILED':
            return Response({
                "task_id": id, 
                "state": "failed", 
                "error": "An error occurred while performing the analysis"
            }) 


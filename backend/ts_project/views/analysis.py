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

        print(serializer.data)
        task = tasks.perform_analysis.delay(serializer.data)
        return Response({"task_id": task.id})


class AnalysisInstanceView(APIView):
    def get(self, request, id): 
        task = tasks.perform_analysis.AsyncResult(id)
        if  task.state == 'PENDING' or task.state == 'PROGRESS' or task.state == 'STARTED':
            return Response({"task_id": id, "state": "pending"})
        elif task.state == 'SUCCESS':
            res = task.result
            return Response({"task_id": id, "state": "success", "result": res})
        elif task.state == 'FAILED':
            return Response({"task_id": id, "state": "failed"}) #add some reason
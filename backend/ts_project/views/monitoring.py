from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Monitor
from ..serializers import MonitorSerializer, MonitorListSerializer
from django.http import Http404


class MonitorListView(APIView):
    def get(self, request):
        all_monitors = Monitor.objects.all()
        serializer = MonitorListSerializer(all_monitors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MonitorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MonitorDetailView(APIView):
    def get_object(self, pk):
        try:
            return Monitor.objects.get(pk=pk)
        except Monitor.DoesNotExist:
            raise Http404

    def get(self, request, monitor_id,):
        monitor = self.get_object(monitor_id)
        serializer = MonitorSerializer(monitor)
        return Response(serializer.data)

    def put(self, request, monitor_id):
        monitor = self.get_object(monitor_id)
        serializer = MonitorSerializer(monitor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, monitor_id):
        monitor = self.get_object(monitor_id)
        monitor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Monitor, NotificationChannel
from ..serializers import MonitorSerializer, MonitorListSerializer, NotificationChannelSerializer
from django.http import Http404


from django.db.models import Count, Q, Max




class MonitorListView(APIView):
    def get(self, request):
        num_detectors = Count('detectors', distinct=True)
        num_incidents = Count('detectors__incidents', distinct=True, filter=Q(detectors__incidents__state='Open'))
        last_incident = Max('detectors__incidents__start')

        all_monitors = Monitor.objects.annotate(num_detectors=num_detectors, num_incidents=num_incidents, last_incident=last_incident)
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



class NotificationChannelView(APIView):
    def get(self, request):
        channels = NotificationChannel.objects.all()
        serializer = NotificationChannelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationChannelDetailView(APIView):
    def delete(self, request, pk):
        channel = NotificationChannel.objects.get(pk=pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

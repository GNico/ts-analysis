from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import PeriodicAnalysis
from ..serializers import PeriodicAnalysisSerializer
from django.http import Http404


class PeriodicAnalysisListView(APIView):
    def get(self, request, monitor_id):
        all_detectors = PeriodicAnalysis.objects.filter(monitor=monitor_id)
        serializer = PeriodicAnalysisSerializer(all_detectors, many=True)
        return Response(serializer.data)

    def post(self, request, monitor_id):
      #  if 'delete' in request.query_params:
      #      return self._bulk_delete(request)
      #  if 'update' in request.query_params:
      #      return self._bulk_update(request)

        data = request.data 
        data['monitor'] = monitor_id
        serializer = PeriodicAnalysisSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #we need to call each save individually to trigger post_save signal
  #  def _bulk_update(self, request):
  #      update_ids = request.data.get('ids', [])
  #      objs = PeriodicAnalysis.objects.filter(analysis_id__in=update_ids)
  #      active = request.data.get('active', None)
  #      alerts_enabled = request.data.get('alerts_enabled', None)
  #      for item in objs:
  #          if (active is not None):
  #              item.active = active
  #          if (alerts_enabled is not None):
  #              item.alerts_enabled = alerts_enabled
  #          item.save()
  #      return Response(status=status.HTTP_201_CREATED)

    #deleting each element individually because bulk delete doesnt call model's delete method
  #  def _bulk_delete(self, request):
  #      delete_ids = request.data.get('ids', [])
  #      objs = PeriodicAnalysis.objects.filter(analysis_id__in=delete_ids)
  #      for item in objs:
  #          item.delete()
  #      return Response(status=status.HTTP_204_NO_CONTENT)



class PeriodicAnalysisDetailView(APIView):
    def get_object(self, monitor_id, pk):
        try:
            return PeriodicAnalysis.objects.filter(monitor=monitor_id).get(pk=pk)
        except PeriodicAnalysis.DoesNotExist:
            raise Http404

    def get(self, request, monitor_id, detector_id):
        detector = self.get_object(monitor_id, detector_id)
        serializer = PeriodicAnalysisSerializer(detector)
        return Response(serializer.data)

    def put(self, request, monitor_id, detector_id):
        detector = self.get_object(monitor_id, detector_id)
        serializer = PeriodicAnalysisSerializer(detector, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, monitor_id, detector_id):
        detector = self.get_object(monitor_id, detector_id)
        detector.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
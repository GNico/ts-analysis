from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import PeriodicAnalysis
from ..serializers import PeriodicAnalysisSerializer
from django.http import Http404


class PeriodicAnalysisListView(APIView):
    def get(self, request):
        all_analysis = PeriodicAnalysis.objects.all()
        serializer = PeriodicAnalysisSerializer(all_analysis, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'update' in request.query_params:
            return self._bulk_update(request)
        serializer = PeriodicAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _bulk_update(self, request):
        print(request.data)
        update_ids = request.data.get('ids', [])
        objs = PeriodicAnalysis.objects.filter(analysis_id__in=update_ids)
        active = request.data.get('active', None)
        alerts_enabled = request.data.get('alerts_enabled', None)
        #not a bulk save because we need to call post_save signal
        for item in objs:
            if (active is not None):
                item.active = active
            if (alerts_enabled is not None):
                item.alerts_enabled = alerts_enabled
            item.save()
        return Response(status=status.HTTP_201_CREATED)



class PeriodicAnalysisDetailView(APIView):
    def get_object(self, pk):
        try:
            return PeriodicAnalysis.objects.get(pk=pk)
        except PeriodicAnalysis.DoesNotExist:
            raise Http404

    def get(self, request, pk,):
        analysis = self.get_object(pk)
        serializer = PeriodicAnalysisSerializer(analysis)
        return Response(serializer.data)

    def put(self, request, pk):
        analysis = self.get_object(pk)
        serializer = PeriodicAnalysisSerializer(analysis, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        analysis = self.get_object(pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
    
from ..serializers import AnalysisSettingsSerializer
from ..models import Analysis
from django.http import Http404


class AnalysisSettingsListView(APIView):
    def get(self, request):
        all_settings = Analysis.objects.all()
        serializer = AnalysisSettingsSerializer(all_settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'delete' in request.query_params:
            return self._bulk_delete(request)
        serializer = AnalysisSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _bulk_delete(self, request):
        delete_ids = request.data.get('ids', [])
        print(delete_ids)
        Analysis.objects.filter(id__in=delete_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalysisSettingsDetailView(APIView):
    def get_object(self, pk):
        try:
            return Analysis.objects.get(pk=pk)
        except Analysis.DoesNotExist:
            raise Http404

    def get(self, request, pk,):
        settings = self.get_object(pk)
        serializer = AnalysisSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request, pk):
        settings = self.get_object(pk)
        serializer = AnalysisSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        settings = self.get_object(pk)
        settings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


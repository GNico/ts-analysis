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
        serializer = PeriodicAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
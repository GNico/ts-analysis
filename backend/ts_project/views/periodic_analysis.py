from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import PeriodicAnalysis


class PeriodicAnalysisListView(APIView):
    def get(self, request):
        all_analysis = Analysis.objects.all()
        serializer = AnalysisSettingsSerializer(all_analysis, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data.get('analysis', ''))
        print(data.get('active', True))
        print(data.get('interval', '1m'))
        return Response("ok response mock")


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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        analysis = self.get_object(pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
    
from ..serializers import PipelineSerializer
from ..models import Pipeline
from django.http import Http404


class PipelineListView(APIView):
    def get(self, request):
        pipelines = Pipeline.objects.all()
        serializer = PipelineSerializer(pipelines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PipelineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PipelineDetailView(APIView):
    def get_object(self, pk):
        try:
            return Pipeline.objects.get(pk=pk)
        except Pipeline.DoesNotExist:
            raise Http404

    def get(self, request, pk,):
        pipeline = self.get_object(pk)
        serializer = PipelineSerializer(pipeline)
        return Response(serializer.data)

    def put(self, request, pk):
        pipeline = self.get_object(pk)
        serializer = PipelineSerializer(pipeline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pipeline = self.get_object(pk)
        pipeline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


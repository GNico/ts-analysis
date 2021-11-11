from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
    
from ..serializers import TestSetSerializer
from ..models import TestSet
from django.http import Http404


class TestSetListView(APIView):
    def get(self, request):
        all_test_sets = TestSet.objects.all()
        serializer = TestSetSerializer(all_test_sets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TestSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestSetDetailView(APIView):
    def get_object(self, pk):
        try:
            return TestSet.objects.get(pk=pk)
        except TestSet.DoesNotExist:
            raise Http404

    def get(self, request, test_id,):
        settings = self.get_object(test_id)
        serializer = TestSetSerializer(settings)
        return Response(serializer.data)

    def put(self, request, test_id):
        test_set = self.get_object(test_id)
        serializer = TestSetSerializer(test_set, data=request.data, partial=True)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_id):
        test_set = self.get_object(test_id)
        test_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


import re
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import anomaly_detector
from . import services

from . import mock_data

class ClientListView(APIView):
    def get(self, request):
        data = services.get_clients_info()
        return Response(data)

    def post(self, request):
        data = request.data
        client_name = data.get('name', '')
        dest_dir = data.get('folder_name', '')
        docs_path = settings.ELASTIC_DATA_INDEX_PATH + dest_dir
        try:
            status_id = services.add_new_client(client_name=client_name, docs_path=docs_path)
        except services.ClientNameAlreadyExists:
            return Response({'error': "There's already a client with the same name"}, status=status.HTTP_409_CONFLICT)
        return Response({'status_id': status_id}, status=status.HTTP_201_CREATED)



class ClientDetailView(APIView):
    def get(self, request, pk):
        return Response({'details': 'some client details'})

    def delete(self, request, pk):
        services.delete_client(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeriesView(APIView):
    def get(self, request, pk):
        data = services.get_series( 
            client_name=pk, 
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            contexts=request.query_params.getlist('contexts', []),             
            tags=request.query_params.getlist('tags', []),             
            interval=request.query_params.get('interval', '1H'))
        return Response(data)


def listToTree(data):
    root = []
    for full_tag in data:
        currentchildren = root  
        tokenized_full_tag = re.split(r'\s|_', full_tag)
        partial_id = ""
        for index, token in enumerate(tokenized_full_tag):
            last = (index == len(tokenized_full_tag) -1) 
            if not partial_id: 
                partial_id = token
            else:
                partial_id = partial_id + "_" + token
            node = next((item for item in currentchildren if item["name"] == token), {})
            if not node:
                node['name'] = token
                node['id'] = partial_id                
                if not last:
                    node['children'] = []
                currentchildren.append(node)
            if not last: 
                key = 'children'
                if not key in node:
                    node['children'] = []
                currentchildren = node['children']
    return root


class TagListView(APIView):
    def get(self, request, pk):
        data = services.get_tags(client_name=pk)      
        response = listToTree(data)
        return Response(response)


class ContextListView(APIView):
    def get(self, request, pk):
        data = services.get_contexts(client_name=pk)
        response = listToTree(data)
        return Response(response)


def anomalies(request):
    #mocking
    data = {
      "series": mock_data.SERIES,
      "anomalies": mock_data.ANOMALIES,
      "trend": mock_data.TREND,
      "baseline": mock_data.BASELINE
    }
    return JsonResponse(data, safe=False)

   #if request.method == 'GET':
    #     requestedName = request.GET.get('name', '')
     #    requestedTags = request.GET.get('tags', '')
      #   requestedContext= request.GET.get('contexts', '')
       #  requestedStart = request.GET.get('start', '')
       #  requestedEnd = request.GET.get('end', '')
        # requestedInterval = request.GET.get('interval', '1H')

#         series = services.get_series(client_name=requestedName, 
 #                                contexts=requestedContext, 
  #                               tags=requestedTags,
   #                              start=requestedStart,
    #                             end=requestedEnd,
     #                            interval=requestedInterval)
      #   anomalies = anomaly_detector.detectAnomalies(series)
       #  return JsonResponse(anomalies, safe=False)

#temporal
def testalgo(request):
    if request.method == 'GET':
        requestedName = request.GET.get('name', '')
        requestedTags = request.GET.get('tags', '')
        requestedContext= request.GET.get('contexts', '')
        requestedStart = request.GET.get('start', '')
        requestedEnd = request.GET.get('end', '')
        requestedInterval = request.GET.get('interval', '1H')
        series = services.get_series(client_name=requestedName,                                 
                                start=requestedStart,
                                end=requestedEnd,
                                contexts=requestedContext, 
                                tags=requestedTags,
                                interval=requestedInterval)


        anomalies = anomaly_detector.testAlgorythms(series)
        return JsonResponse(anomalies, safe=False)

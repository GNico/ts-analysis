from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import anomaly_detector
from . import data_path
from . import services


class ClientsView(APIView):
    def get(self, request):
        data = services.get_clients_info()
        return Response(data)

    def post(self, request):
        data = request.data
        client_name = data.get('name', '')
        dest_dir = data.get('folder_name', '')
        docs_path = data_path.DATA_PATH + dest_dir
        try:
            status_id = services.add_new_client(client_name=client_name, docs_path=docs_path)
        except services.ClientNameAlreadyExists:
            return Response({'error': "There's already a client with the same name"}, status=status.HTTP_409_CONFLICT)
        return Response({'status_id': status_id}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        services.delete_client(request.query_params.get('name', ''))
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeriesView(APIView):
    def get(self, request, pk):
        data = services.get_series( 
            client_name=pk, 
            context=request.query_params.get('tags', ''), 
            tags=request.query_params.get('contexts', ''),
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            interval=request.query_params.get('interval', '1H') )
        return Response(data)


class TagListView(APIView):
    def get(self, request, pk):
        data = services.get_tags(client_name=pk)
        return Response(data)


class ContextListView(APIView):
    def get(self, request, pk):
        data = services.get_contexts(client_name=pk)
        return Response(data)


def anomalies(request):
    #mocking
    #data = {
    #  "anomalies": mock_data.ANOMALIES,
    #  "trend": mock_data.TREND,
    #  "baseline": mock_data.BASELINE
    #}

    #return JsonResponse(data, safe=False) 
    if request.method == 'GET':
         requestedName = request.GET.get('name', '')
         requestedTags = request.GET.get('tags', '')
         requestedContext= request.GET.get('contexts', '')
         requestedStart = request.GET.get('start', '')
         requestedEnd = request.GET.get('end', '')
         requestedInterval = request.GET.get('interval', '1H')

         series = services.get_series(clientname=requestedName, 
                                 context=requestedContext, 
                                 tags=requestedTags,
                                 start=requestedStart,
                                 end=requestedEnd,
                                 interval=requestedInterval)
         anomalies = anomaly_detector.detectAnomalies(series)
         return JsonResponse(anomalies, safe=False)



#temporal
def testalgo(request):
    if request.method == 'GET':
        requestedName = request.GET.get('name', '')
        requestedTags = request.GET.get('tags', '')
        requestedContext= request.GET.get('contexts', '')
        requestedStart = request.GET.get('start', '')
        requestedEnd = request.GET.get('end', '')
        requestedInterval = request.GET.get('interval', '1H')
        series = services.get_series(clientname=requestedName, 
                                context=requestedContext, 
                                tags=requestedTags,
                                start=requestedStart,
                                end=requestedEnd,
                                interval=requestedInterval)

        anomalies = anomaly_detector.testAlgorythms(series)
        return JsonResponse(anomalies, safe=False)

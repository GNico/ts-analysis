from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.template import loader
import json
#from elasticsearch import Elasticsearch
from . import anomaly_detector
from . import data_path
#from . import mock_data
from . import services
#from .tasks import long_task

def index(request):
    return render(request, 'prueba/index.html')

def clients(request):
    if request.method == 'GET':
        data = services.get_clients_info()
        return JsonResponse(data, safe=False)

def clientnames(request):
    if request.method == 'GET':
        data = services.get_clients_names()
        return JsonResponse(data, safe=False)


@api_view(['POST'])
def newclient(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        client_name = data.get('name', '')
        #index_name = data.get('index_name', '')
        dest_dir = data.get('folder_name', '')
        docs_path = data_path.DATA_PATH + dest_dir

        status_id = services.add_new_client(client_name=client_name, docs_path=docs_path)
        return JsonResponse({ 'status_id': status_id }, safe=False)


#returns list of tags
def tags(request):
    if request.method == 'GET':
        clientname = request.GET.get('name', '')
        data = services.get_tags(client_name=clientname)
        return JsonResponse(data, safe=False)

#returns list of contexts
def contexts(request):
    if request.method == 'GET':
        clientname = request.GET.get('name', '')
        data = services.get_contexts(client_name=clientname)
        return JsonResponse(data, safe=False)        


def series(request):
    #return JsonResponse(mock_data.SERIES, safe=False) 
    if request.method == 'GET':
        requestedName = request.GET.get('name', '')
        requestedTags = request.GET.get('tags', '')
        requestedContext= request.GET.get('contexts', '')
        requestedStart = request.GET.get('start', '')
        requestedEnd = request.GET.get('end', '')
        requestedInterval = request.GET.get('interval', '1H')
        data = services.get_series(client_name=requestedName, 
                            context=requestedContext, 
                            tags=requestedTags,
                            start=requestedStart,
                            end=requestedEnd,
                            interval=requestedInterval)
        return JsonResponse(data, safe=False)


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


'''

def longtask(request):
    task = long_task.apply_async()
    return JsonResponse({'task_id': task.id}, safe=False)


def taskstatus(request, task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return JsonResponse(response, safe=False) 

'''
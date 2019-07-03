from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.template import loader
import json
from elasticsearch import Elasticsearch

from . import anomaly_detector
from . import elastic_helper
from . import data_path
from . import mock_data


def index(request):
    return render(request, 'prueba/index.html')


def clients(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        data = es.getClients()
        return JsonResponse(data, safe=False)

@api_view(['POST'])
def newclient(request):
    es = elastic_helper.EsHelper()
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        clientName = data.get('name', '')
        index_name = data.get('index_name', '')
        destDir = data.get('folder_name', '')
        docspath = data_path.DATA_PATH + destDir

        result = es.addNewClient(clientname=clientName, indexname=index_name, docspath=docspath)
        data = json.dumps(result)
        data = { 'name': 'asd' }
        return JsonResponse(data, safe=False)


#returns list of tags
def tags(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        clientname = request.GET.get('name', '')
        data = es.getTags(clientname=clientname)
        return JsonResponse(data, safe=False)

#returns list of contexts
def contexts(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        clientname = request.GET.get('name', '')
        data = es.getContexts(clientname=clientname)
        return JsonResponse(data, safe=False)        


def series(request):

    #return JsonResponse(mock_data.SERIES, safe=False) 
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        requestedName = request.GET.get('name', '')
        requestedTags = request.GET.get('tags', '')
        requestedContext= request.GET.get('contexts', '')
        requestedStart = request.GET.get('start', '')
        requestedEnd = request.GET.get('end', '')
        requestedInterval = request.GET.get('interval', '1H')
        data = es.getSeries(clientname=requestedName, 
                                context=requestedContext, 
                                tags=requestedTags,
                                start=requestedStart,
                                end=requestedEnd,
                                interval=requestedInterval)
        return JsonResponse(data, safe=False)


def anomalies(request):
    #mocking
    data = {
      "anomalies": mock_data.ANOMALIES,
      "trend": mock_data.TREND,
      "baseline": mock_data.BASELINE
    }

    return JsonResponse(data, safe=False) 


    # es = elastic_helper.EsHelper()
    # if request.method == 'GET':
    #     requestedName = request.GET.get('name', '')
    #     requestedTags = request.GET.get('tags', '')
    #     requestedContext= request.GET.get('contexts', '')
    #     requestedStart = request.GET.get('start', '')
    #     requestedEnd = request.GET.get('end', '')
    #     requestedInterval = request.GET.get('interval', '1H')

    #     series = es.getSeries(clientname=requestedName, 
    #                             context=requestedContext, 
    #                             tags=requestedTags,
    #                             start=requestedStart,
    #                             end=requestedEnd)

    #     data = anomaly_detector.detectAnomalies(series)
    #     return JsonResponse(data, safe=False)


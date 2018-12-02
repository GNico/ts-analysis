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


def index(request):
    parametro = 'nico'
    context = {'parametro': parametro,}
    return render(request, 'prueba/index.html', context)


def clients(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        jsondata = es.getClients()
        return JsonResponse(jsondata, safe=False)

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
        jsondata = json.dumps(result)
        jsondata = { 'name': 'asd' }
        return JsonResponse(jsondata, safe=False)


#returns list of tags
def tags(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        jsondata = es.getTags(clientname="movistar")
        return JsonResponse(jsondata, safe=False)


def series(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        requestedTag = request.GET.get('tag', '')
        jsondata = es.getSeries(clientname="movistar", tags=[requestedTag])
        return JsonResponse(jsondata, safe=False)


def anomaly(request):
    client = Elasticsearch()
    if request.method == 'GET':
        requestedTag = request.GET.get('tag', '')

        if requestedTag:
            query = {
                "query": {
                    "match": {
                        "tag": requestedTag
                    }
                },
                "aggs": {
                    "my_aggregation": {
                        "date_histogram": {
                            "field":     "@timestamp",
                            "interval":  "30m"
                        }
                    }
                }
            }
        else:
            query = {
                "aggs": {
                    "my_aggregation": {
                        "date_histogram": {
                            "field":     "@timestamp",
                            "interval":  "30m"
                        }
                    }
                }
            }

        response = client.search(index="movi*", size=0, body=query)

        jsondata = anomaly_detector.detectAnomalies(response)

        return JsonResponse(jsondata, safe=False)


from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
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


def newclient(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        clientName = request.GET.get('name', '')
        destDir = request.GET.get('dir', '')
        docspath = data_path.DATA_PATH + docsdir
        result = es.addNewClient(clientname=clientName, docspath=docspath)
        jsondata = json.dumps(result)
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


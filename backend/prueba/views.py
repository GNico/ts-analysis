from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import json
from elasticsearch import Elasticsearch

from . import anomaly_detector

def index(request):
    parametro = 'nico'
    context = {'parametro': parametro,}
    return render(request, 'prueba/index.html', context)


#returns list of tags
def tags(request):
    client = Elasticsearch()
    if request.method == 'GET':
        query_tags = {
            "aggs": {
                "my_aggregation": {
                    "terms":  { 
                        "field" : "tag.keyword",
                        "size": 10000
                    }
                }
            }
        }
        response = client.search(index="movi*", size=0, body=query_tags)
        jsondata = [] 
        for element in response['aggregations']['my_aggregation']['buckets']:
            jsondata.append(element['key'])

        return JsonResponse(jsondata, safe=False)


def series(request):
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
        jsondata = [] 
        for element in response['aggregations']['my_aggregation']['buckets']:
            jsondata.append([element['key'], element['doc_count']])

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


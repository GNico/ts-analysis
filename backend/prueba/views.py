from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import json

from . import anomaly_detector
from . import elastic_helper

def index(request):
    parametro = 'nico'
    context = {'parametro': parametro,}
    return render(request, 'prueba/index.html', context)


def clients(request):
    if request.method == 'GET':
        jsondata = [
        {
            'name': 'Movistar',
            'context': ['Facebook', 'Twitter', 'Instagram'],
            'count': 2170000,
            'start_date': '2/10/2017',
            'end_date': '28/2/2018'
        },
        {
            'name': 'Fravega',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'Banco Galicia',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'GCBA',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'Presidencia',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'Provincia',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'Despegar - BR',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        },
        {
            'name': 'Despegar - ES',
            'context': ['Twitter', 'Facebook', 'Webpage'],
            'count': 500000,
            'start_date': '3/11/2017',
            'end_date': '1/3/2018'
        }]
        return JsonResponse(jsondata, safe=False)


def newclient(request):
    es = elastic_helper.EsHelper()
    if request.method == 'GET':
        clientName = request.GET.get('name', '')
        destDir = request.GET.get('dir', '')
        result = es.indexDocuments(clientName, destDir)
        jsondata = json.dumps(result)
        return JsonResponse(jsondata, safe=False)


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


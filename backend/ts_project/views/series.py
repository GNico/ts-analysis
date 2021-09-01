from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..elastic import series_search
from ..models import Client

search = series_search.SeriesSearch()

def filter_series_params(request):
    if 'tags' not in request.query_params:
        tags = None
    elif request.query_params['tags'] == '':
        tags = []
    else:
        tags =  request.query_params.getlist('tags', [])

    if 'contexts' not in request.query_params:
        contexts = None
    elif request.query_params['contexts'] == '':
        contexts = []
    else:
        contexts =  request.query_params.getlist('contexts', [])
    return (tags, contexts)


class SeriesView(APIView):
    def get(self, request, pk):
        tags, contexts = filter_series_params(request)
        client = Client.objects.get(name=pk)
        data = search.get_series(
            indexname=client.index_name, 
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            context=contexts,             
            tags=tags,             
            interval=request.query_params.get('interval', '1h'),
            filter_tags=request.query_params.get('filterTags', False),
            filter_contexts=request.query_params.get('filterContexts', False))
        return Response(data)


class TagCountView(APIView):
    def get(self, request, pk):
        tags, contexts = filter_series_params(request)
        client = Client.objects.get(name=pk)
        data = search.get_tags_count(
            indexname=client.index_name, 
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            context=contexts,             
            tags=tags,             
            size=request.query_params.get('size', 20),
            filter_tags=request.query_params.get('filterTags', False),
            filter_contexts=request.query_params.get('filterContexts', False))
        return Response(data)


class TagListView(APIView):
    def get(self, request, pk):
        client = Client.objects.get(name=pk)
        data = search.get_tags(client.index_name)
        response = listToTree(data)
        return Response(response)


class ContextListView(APIView):
    def get(self, request, pk):
        client = Client.objects.get(name=client_name)
        data = search.get_contexts(client.index_name)
        response = listToTree(data)
        return Response(response)


def listToTree(data):
    import re
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
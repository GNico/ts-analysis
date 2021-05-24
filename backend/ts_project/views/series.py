from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services


class SeriesView(APIView):
    def get(self, request, pk):
        data = services.get_series( 
            client_name=pk, 
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            contexts=request.query_params.getlist('contexts', []),             
            tags=request.query_params.getlist('tags', []),             
            interval=request.query_params.get('interval', '1h'))
        return Response(data)


class TagCountView(APIView):
    def get(self, request, pk):
        data = services.get_tags_count(
            client_name=pk, 
            start=request.query_params.get('start', ''),
            end=request.query_params.get('end', ''),
            contexts=request.query_params.getlist('contexts', []),             
            tags=request.query_params.getlist('tags', []),             
            size=request.query_params.get('size', 20))
        return Response(data)


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
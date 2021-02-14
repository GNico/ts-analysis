from rest_framework.response import Response
from rest_framework.views import APIView

from ..salib.model.pipeline.node_factory import NodeFactory

class PipelineNodesListView(APIView):
    
    def get(self, request):
        return Response(NodeFactory.nodes_list())

class PipelineNodesDetailView(APIView):

    def get(self, request, group, type):
        return Response(NodeFactory.node_description(group, type))
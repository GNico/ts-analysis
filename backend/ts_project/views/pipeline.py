from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
    
from ..salib.model.pipeline.pipeline import Pipeline
from ..salib.model.pipeline.node_factory import NodeFactory

class PipelineView(APIView):

    def get(self, request):
        transformers = NodeFactory.nodes_description('transformer')
        detectors = NodeFactory.nodes_description('detector')
        aggregators = NodeFactory.nodes_description('aggregator')
        return Response([*transformers, *detectors, *aggregators])

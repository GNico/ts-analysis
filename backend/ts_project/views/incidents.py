from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Incident
from ..serializers import IncidentListSerializer
from django.http import Http404


class IncidentsListView(APIView):
    def get(self, request):
        all_incidents = Incident.objects.all()
        serializer = IncidentListSerializer(all_incidents, many=True)
        return Response(serializer.data)

    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Incident
from ..serializers import IncidentListSerializer, IncidentSerializer
from django.http import Http404


class IncidentsListView(APIView):
    def get(self, request):
        all_incidents = Incident.objects.all()
        serializer = IncidentListSerializer(all_incidents, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'delete' in request.query_params:
            return self._bulk_delete(request)
        if 'update' in request.query_params:
            return self._bulk_update(request)

        serializer = IncidentSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _bulk_update(self, request):
        update_ids = request.data.get('ids', [])
        objs = Incident.objects.filter(id__in=update_ids)
        state = request.data.get('state', None)
        for item in objs:
            if (state is not None):
                item.state = state
            item.save()
        return Response(status=status.HTTP_201_CREATED)

    def _bulk_delete(self, request):
        delete_ids = request.data.get('ids', [])
        objs = Incident.objects.filter(id__in=delete_ids).delete()
       # for item in objs:
       #     item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncidentDetailView(APIView):
    def get_object(self, incident_id):
        try:
            return Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404

    def get(self, request, incident_id):
        incident = self.get_object(incident_id)
        serializer = IncidentSerializer(incident)
        return Response(serializer.data)

    def put(self, request, incident_id):
        incident = self.get_object(incident_id)
        serializer = IncidentSerializer(incident, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, incident_id):
        incident = self.get_object(incident_id)
        incident.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




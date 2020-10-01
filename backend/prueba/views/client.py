from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services

class ClientListView(APIView):
    def get(self, request):
        data = services.get_clients_info()
        return Response(data)

    def post(self, request):
        data = request.data
        client_name = data.get('name', '')
        dest_dir = data.get('folder_name', '')
        docs_path = settings.ELASTIC_DATA_INDEX_PATH + dest_dir
        try:
            status_id = services.add_new_client(client_name=client_name, docs_path=docs_path)
        except services.ClientNameAlreadyExists:
            return Response({'error': "There's already a client with the same name"}, status=status.HTTP_409_CONFLICT)
        return Response({'status_id': status_id}, status=status.HTTP_201_CREATED)


class ClientView(APIView):
    def get(self, request, pk):
        return Response({'details': 'some client details'})

    def delete(self, request, pk):
        services.delete_client(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

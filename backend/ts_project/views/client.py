from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import services
from .. import utils
from .. import serializers

class ClientListView(APIView):
    def get(self, request):
        data = services.get_clients_info()
        return Response(data)

    def post(self, request):
        serializer = serializers.ClientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_name = serializer.data.get('name')
        dest_dir = serializer.data.get('folder_name')
        docs_path = utils.get_data_source_path() + dest_dir
        try:
            status_id = services.add_new_client(client_name=client_name, docs_path=docs_path)
        except services.ClientNameAlreadyExists:
            return Response({'error': "There's already a client with the same name"}, status=status.HTTP_409_CONFLICT)
        return Response({'status_id': status_id}, status=status.HTTP_201_CREATED)


class ClientView(APIView):
    def get(self, request, pk):
        data = services.get_client_details(pk)
        return Response(data)

    def delete(self, request, pk):
        services.delete_client(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataSourceFilesList(APIView):
    def get(self, request):
        source_files_path = utils.get_data_source_path()
        return Response(utils.get_dirs_from_dir(source_files_path))
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..elastic import series_indexer, series_search
from ..models import Client
from ..serializers import ClientInputSerializer, ClientEditSerializer
from .. import tasks, task_priorities, utils, serializers

search = series_search.SeriesSearch()
indexer = series_indexer.SeriesIndexer()

class ClientNameAlreadyExists(Exception):
    pass

class ClientListView(APIView):
    def get(self, request):
        #update indexing progress
        indexing_clients = []
        indexed_clients =  []
        clients_objs = Client.objects.filter(status='Pending')
        for client in clients_objs:
            task = tasks.index_series_data.AsyncResult(client.task_id)
            if task.state == 'PROGRESS' or task.state == 'STARTED':
                indexing_clients.append({
                    'name': client.name,
                    'utc_offset': client.utc_offset,
                    'status': 'Indexing',
                    'progress': task.info.get('progress', 0)
                })
            elif task.state == 'PENDING':
                indexing_clients.append({
                    'name': client.name,
                    'utc_offset': client.utc_offset,
                    'status': 'Waiting',
                    'progress': 0
                })
        indexed_clients = Client.objects.exclude(status='Pending').values('name', 'utc_offset', 'status', 'created', 'modified')
        data = [ *indexing_clients, *indexed_clients ]
        return Response(data)

    def post(self, request):
        serializer = ClientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dest_dir = serializer.data.get('folder_name')
        try:
            status_id = self._add_new_client(
                client_name=serializer.data.get('name'), 
                dest_dir=dest_dir, 
                utc_offset=serializer.data.get('utc_offset')
            )
        except ClientNameAlreadyExists:
            return Response({'error': "There's already a client with the same name"}, status=status.HTTP_409_CONFLICT)
        return Response({'status_id': status_id}, status=status.HTTP_201_CREATED)


    def _add_new_client(self, client_name, dest_dir, utc_offset):
        if Client.objects.filter(name=client_name).exists():
            raise ClientNameAlreadyExists()
        docs_path = utils.get_data_source_path() + dest_dir
        filenames = utils.get_files_from_directory(docs_path)
        task = tasks.index_series_data.delay(client_name, filenames)
        task = tasks.index_series_data.apply_async(args=[client_name, filenames], priority=task_priorities.INDEXING)
        client = Client.objects.create(
            name=client_name, 
            utc_offset=utc_offset, 
            index_name='', 
            task_id=task.id, 
            status='Pending'
        )
        return task.id


class ClientView(APIView):
    def get(self, request, pk):
        client = Client.objects.get(name=pk)
        utc_offset = client.utc_offset
        series_data = search.get_series(indexname=client.index_name, interval='7d')
        series_range = search.get_series_range(indexname=client.index_name)
        total_events = search.get_count(indexname=client.index_name)
        last_events = search.get_last_events(indexname=client.index_name, size=20)
        data = { 'data': series_data, 'range': series_range, 'total': total_events, 'lastEvents': last_events }
        return Response(data)

    def put(self, request, pk):
        client = Client.objects.get(name=pk)
        serializer = ClientEditSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = Client.objects.filter(name=pk).delete()
        indexer.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataSourceFilesList(APIView):
    def get(self, request):
        source_files_path = utils.get_data_source_path()
        return Response(utils.get_dirs_from_dir(source_files_path))
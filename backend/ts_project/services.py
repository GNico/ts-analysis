from .models import Client
from .elastic import series_search, series_indexer
from . import tasks
from . import task_priorities
from . import utils

search = series_search.SeriesSearch()
indexer = series_indexer.SeriesIndexer()

class ClientNameAlreadyExists(Exception):
    pass


def add_new_client(client_name, docs_path):
    if Client.objects.filter(name=client_name).exists():
        raise ClientNameAlreadyExists()
    filenames = utils.get_files_from_directory(docs_path)
    task = tasks.index_series_data.delay(client_name, filenames)
    task = tasks.index_series_data.apply_async(args=[client_name, filenames], priority=task_priorities.INDEXING)
    client = Client.objects.create(name=client_name, index_name='', task_id=task.id, status='Pending')
    return task.id
   

def delete_client(client_name):
    client = Client.objects.filter(name=client_name).delete()
    indexer.delete(client_name)


def get_clients_info():
    #update indexing progress
    indexing_clients = []
    indexed_clients =  []
    clients_objs = Client.objects.filter(status='Pending')
    for client in clients_objs:
        task = tasks.index_series_data.AsyncResult(client.task_id)
        if task.state == 'PROGRESS' or task.state == 'STARTED':
            indexing_clients.append({
                'name': client.name,
                'status': 'Indexing',
                'progress': task.info.get('progress', 0)
            })
        elif task.state == 'PENDING':
            indexing_clients.append({
                'name': client.name,
                'status': 'Waiting',
                'progress': 0
            })
    indexed_clients = Client.objects.exclude(status='Pending').values('name', 'status', 'created', 'modified')
    return [ *indexing_clients, *indexed_clients ]


def get_client_details(client_name):
    client = Client.objects.get(name=client_name)
    series_data = search.get_series(indexname=client.index_name, interval='7d')
    series_range = search.get_series_range(indexname=client.index_name)
    total_events = search.get_count(indexname=client.index_name)
    last_events = search.get_last_events(indexname=client.index_name, size=20)
    return { 'data': series_data, 'range': series_range, 'total': total_events, 'lastEvents': last_events }


def get_series(client_name, start, end, contexts, tags, interval, filter_tags, filter_contexts):
    client = Client.objects.get(name=client_name)
    return search.get_series(client.index_name, start, end, contexts, tags, interval, filter_tags, filter_contexts)


def get_tags_count(client_name, start, end, contexts, tags, size, filter_tags, filter_contexts):
    client = Client.objects.get(name=client_name)
    return search.get_tags_count(client.index_name, start, end, contexts, tags, size, filter_tags, filter_contexts)


def get_tags(client_name):
    client = Client.objects.get(name=client_name)
    return search.get_tags(client.index_name)


def get_contexts(client_name):
    client = Client.objects.get(name=client_name)
    return search.get_contexts(client.index_name)



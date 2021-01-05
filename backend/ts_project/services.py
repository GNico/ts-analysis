from math import ceil
from .models import Client
from .elastic import series_search, series_indexer
from . import tasks
from . import utils

search = series_search.SeriesSearch()
indexer = series_indexer.SeriesIndexer()

class ClientNameAlreadyExists(Exception):
    pass


def add_new_client(client_name, docs_path):
    if not Client.objects.filter(name=client_name).exists():
        filenames = utils.get_files_from_directory(docs_path)
        task = tasks.index_series_data.apply_async((client_name, filenames))
        client = Client.objects.create(name=client_name, index_name='', task_id=task.id, indexing=True)
        return task.id
    else:
        raise ClientNameAlreadyExists()


def delete_client(client_name):
    client = Client.objects.filter(name=client_name).delete()
    indexer.delete(client_name)


def get_clients_info():
    #update indexing progress
    indexing_clients = []
    clients_objs = Client.objects.filter(indexing=True)
    for obj in clients_objs:
        task = tasks.index_series_data.AsyncResult(obj.task_id)
        if task.state == 'PROGRESS':
            indexing_clients.append({
                'name': obj.name,
                'indexing': True,
                'created': obj.created,
                'progress': _calculate_progress(task)
            })
        elif task.state == 'SUCCESS':
            obj.indexing = False
            obj.task_id = ''
            obj.save()

    ready_clients = Client.objects.filter(indexing=False).values('name', 'indexing', 'created', 'modified')
    return [ *indexing_clients, *ready_clients ]


def get_client_details(client_name):
    client = Client.objects.get(name=client_name)
    series_data = search.get_series(indexname=client.index_name, interval='7d')
    series_range = search.get_series_range(indexname=client.index_name)
    tags_count = search.get_tags(indexname=client.index_name)
    return { 'data': series_data, 'range': series_range, 'tagsCount': len(tags_count) }


def get_series(client_name, start, end, contexts, tags, interval):
    client = Client.objects.get(name=client_name)
    return search.get_series(client.index_name, start, end, contexts, tags, interval)


def get_tags_count(client_name, start, end, contexts, tags, size):
    client = Client.objects.get(name=client_name)
    return search.get_tags_count(client.index_name, start, end, contexts, tags, size)


def get_tags(client_name):
    client = Client.objects.get(name=client_name)
    return search.get_tags(client.index_name)


def get_contexts(client_name):
    client = Client.objects.get(name=client_name)
    return search.get_contexts(client.index_name)


def _calculate_progress(task):
    total = task.info.get('total_events', 1)
    current = search.get_count(task.info.get('index_name'))
    return ceil(current * 100 / total)



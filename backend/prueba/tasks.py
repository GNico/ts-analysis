from celery import shared_task
import json

from .elastic import series_indexer
from .models import Client

@shared_task()
def addtask():
    return 5

@shared_task(bind=True)
def index_series_data(self, client_name, filenames):
    indexer = series_indexer.SeriesIndexer()
    self.update_state(state='PROGRESS',
                      meta={'client_name': client_name, 
                            'index_name': indexer.get_index_name(client_name), 
                            'total_events': count_total_events(filenames) 
                            })
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)
            indexer.index(client_name, data)

    client = Client.objects.get(name=client_name)
    client.index_name = indexer.get_index_name(client_name)
    client.task_id = ''
    client.indexing = False
    client.save()


def count_total_events(filenames):
    total = 0
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)
            total += len(data)
    return total
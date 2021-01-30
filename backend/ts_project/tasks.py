from celery import shared_task
from celery import Task
import json

from .elastic import series_indexer
from .models import Client


class ClientIndexingTask(Task):
    def __call__(self, *args, **kwargs):
        self.indexer = series_indexer.SeriesIndexer()

        res = self.run(*args, **kwargs)

        self.update_state(
            state='PROGRESS',
            meta = { 
                'client_name': args[0], 
                'index_name': self.indexer.get_index_name(args[0]), 
                'total_events': count_total_events(args[1])}
        )
        try:
            for filename in args[1]:
                with open(filename) as f:
                    data = json.load(f)
                    self.indexer.index(args[0], data)
        except series_indexer.IndexingError:
            print('fail')
        return res

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("FAILED TASK")
        client = Client.objects.get(name=args[0])
        client.index_name = self.indexer.get_index_name(args[0])
        client.task_id = ''
        client.status = 'Failed'
        client.save()

    def on_success(self, retval, task_id, args, kwargs):
        print("Successful task")
        client = Client.objects.get(name=args[0])
        client.index_name = self.indexer.get_index_name(args[0])
        client.task_id = ''
        client.status = 'Ready'
        client.save()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('Task returned after')
        print(args[0])



@shared_task(bind=True, base=ClientIndexingTask)
def index_series_data(self, client_name, filenames):
    print("do nothing")



def count_total_events(filenames):
    total = 0
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)
            total += len(data)
    return total
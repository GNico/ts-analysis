from celery import shared_task
from celery import Task
import json
from math import ceil
import os
from .elastic import series_indexer
from .models import Client


class ClientIndexingTask(Task):
    def __call__(self, *args, **kwargs):
        self.indexer = series_indexer.SeriesIndexer()
        self.run(*args, **kwargs) #calls task function annotated with @shared_task
        self._update_progress(args[0], 0)
        total_size = self._count_total_files_size(args[1])
        processed_size = 0
        try:
            for filename in args[1]:
                with open(filename) as f:
                    data = json.load(f)
                    self.indexer.index(args[0], data)
                    processed_size += os.path.getsize(str(filename))
                    self._update_progress(args[0], self._calculate_progress(total_size, processed_size))
        except series_indexer.IndexingError:
            print('INDEXING ERROR')

    def _count_total_files_size(self, filenames):
        total = 0
        for filename in filenames:
            total += os.path.getsize(str(filename))
        return total

    def _calculate_progress(self, total, current):
        progress = ceil(current * 100 / total)
        return progress

    def _update_progress(self, client, progress):
        self.update_state(
            state='PROGRESS',
            meta = { 
                'progress': progress,
            }
        )

    #override
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("FAILED TAsSK")
        client = Client.objects.get(name=args[0])
        client.index_name = self.indexer.get_index_name(args[0])
        client.task_id = ''
        client.status = 'Failed'
        client.save()

    #override
    def on_success(self, retval, task_id, args, kwargs):
        print("SUCCESFULL TASK")
        client = Client.objects.get(name=args[0])
        client.index_name = self.indexer.get_index_name(args[0])
        client.task_id = ''
        client.status = 'Ready'
        client.save()

    #override
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('Task returned after')
        print(args[0])



@shared_task(bind=True, base=ClientIndexingTask)
def index_series_data(self, client_name, filenames):
    print("do nothing")


from celery import shared_task
import os
import json

from .elastic import series_indexer

@shared_task
def adding_task(x, y):
    return x + y

'''@shared_task(bind=True)
def long_task(self):
    
    testmodel = TestModel(first_name="new", last_name="name")
    testmodel.save()

    #Read ALL entries
    objects = TestModel.objects.all()   
    for elt in objects:
      print(elt.first_name)

    total = 30
    for i in range(total):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total})
        time.sleep(1)
    return {'current': total, 'total': total, 'status': 'Task completed!'} '''


@shared_task(bind=True)
def index_series_data(self, client_name, docs_path):
    #calculate total events in source files to estimate index progress
    total = 0
    files = [ f for f in os.listdir(docs_path) if os.path.isfile(os.path.join(docs_path,f)) ]
    for filename in files:
        with open(os.path.join(docs_path,filename)) as f:
            data = json.load(f)
            total += len(data)

    print("total docs: ")
    print(total)

    indexer = series_indexer.SeriesIndexer(client_name)
    self.update_state(state='PROGRESS',
                      meta={'client_name': client_name, 
                            'index_name': indexer.get_index_name(), 
                            'total_events': total})
    indexer.index_from_files(docs_path)

    return "done"
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.client import IngestClient
import json
import os
from . import data_path

class EsHelper():
    conn = ""
    index_name = ""
    pipeline_id = ""
    datadir = data_path.DATA_PATH


    def __init__(self):
        self.conn = Elasticsearch(['localhost:9200'])

    #---------------------------SEARCHING--------------------------------------------

    #---------------------------INDEXING---------------------------------------------

    #data from new client must be in the folder "docsdir"
    def addNewClient(self, indexname, docsdir):
        result = ''
        self.index_name = indexname
        self._createPipeline()
        docspath = self.datadir + docsdir
        files = [ f for f in os.listdir(docspath) if os.path.isfile(os.path.join(docspath,f)) ]
        for filename in files:
            with open(os.path.join(docspath,filename)) as f:
                data = json.load(f)
                result = bulk(self.conn, self._makeDocuments(data))
        return result


    #generator to iterate over all documents
    def _makeDocuments(self, data):
        for event in data:
            doc = {
                    '_index': self.index_name,
                    '_type': 'document',
                    '_id': event['_id'],
                    'pipeline': self.pipeline_id,
                    '_source': {'id': event['_id'], 
                                '@timestamp': event['source']['date'], 
                                'tag': event['source']['tags'],
                                'context': event['source']['context']
                               }
            }
            yield(doc) 


    #must be called before indexing to automatically group indices by week
    def _createPipeline(self):
        ic = IngestClient(self.conn)
        self.pipeline_id = 'weeklyprocessor'
        pipeline_body = {
                      "description": "weekly date-time index naming",
                      "processors" : [
                        {
                          "date_index_name" : {
                            "field" : "@timestamp",
                            "index_name_prefix" : self.index_name + "-",
                            "date_rounding" : "w",
                          }
                        }
                      ]
        }
        ic.put_pipeline(id=self.pipeline_id, body=pipeline_body)

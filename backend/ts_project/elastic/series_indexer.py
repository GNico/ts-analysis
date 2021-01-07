from elasticsearch.helpers import bulk
from elasticsearch.helpers.errors import BulkIndexError
from elasticsearch.client import IngestClient
import json
import os
from .es_connection import es

class IndexingError(Exception):
    pass

class SeriesIndexer():
    index_prefix = "ts-"                        #prefix added to the name of data indices 
    series_template_name = "series_template"

    def __init__(self):
        self._create_template()
        self.pipeline_id = self._create_pipeline()

    def get_index_name(self, name):
        return self.index_prefix + name

    def index(self, name, data):      
        try:
            bulk(es, self._make_documents(name, data))
        except Exception:   #BulkIndexError
            raise(IndexingError)
           
    def delete(self, name):
        index_pattern = self.get_index_name(name) + '-*'
        es.indices.delete(index=index_pattern)

    #index template for series data
    def _create_template(self):
        if not es.indices.exists_template(self.series_template_name):
            index_pattern = [ self.index_prefix + '*' ]
            body =  {
                "index_patterns" :  index_pattern,
                "settings" : {
                  "index" : {
                    "sort.field" : "@timestamp", 
                    "sort.order" : "desc" 
                  },
                  "analysis": {
                    "analyzer": {
                      "tag_tree": {
                        "tokenizer": "tag_hierarchy"
                      }
                    },
                    "tokenizer": {
                      "tag_hierarchy": {
                        "type": "path_hierarchy",
                        "delimiter": "_",
                      }
                    }
                  }
                },
                "mappings": {                    
                  "properties": {
                    "@timestamp": {
                      "type": "date"
                    },
                    "tag": {
                      "type": "keyword",
                      "fields": {
                        "tree": {
                          "type": "text",
                          "analyzer": "tag_tree"
                        }
                      }
                    },
                    "context": {
                      "type": "keyword"
                    }
                  }                    
                }
            }
            es.indices.put_template(name=self.series_template_name, body=body)

    #pipeline to automatically create monthly indices
    def _create_pipeline(self):   
        ic = IngestClient(es)
        pipeline = 'monthlyprocessor'
        pipeline_body = {
                      "description": "monthly date-time index naming",
                      "processors" : [
                        {
                          "date_index_name" : {
                            "field" : "@timestamp",
                            "index_name_prefix" : "{{ _index}}-",
                            "date_rounding" : "M",
                          }
                        }
                      ]
        }
        ic.put_pipeline(id=pipeline, body=pipeline_body)
        return pipeline

    #generator to iterate over all events and define doc structure
    def _make_documents(self, name, data):
        for event in data:
            doc = {
                    '_index': self.get_index_name(name),
                    '_id': event['_id'],
                    'pipeline': self.pipeline_id,
                    '_source': {
                      '@timestamp': event['source']['date'], 
                      'tag': event['source']['tags'],
                      'context': event['source']['context']
                    }
            }
            yield(doc) 

    def _clean_index_name(self, name):
        return name.strip(' _\n\t').lower().replace(" ", "")

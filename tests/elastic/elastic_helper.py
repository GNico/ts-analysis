from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.client import IngestClient
import json
import os

class EsHelper():
    conn = ""
    index_prefix = "ts-"                        #prefix added to the name of data indices 
    index_name = ""                             #index containing series data
    pipeline_id = ""            
    client_index_name = "clients"               #index containing clients and their index info
    series_template_name = "series_template"    #template used to index series data


    def __init__(self):
        self.conn = Elasticsearch(['localhost:9200'])
        #create index to store clients if it doesn't exist already
        if not self.conn.indices.exists(self.client_index_name):
            self.conn.indices.create(index=self.client_index_name, 
                                    body= {
                                        "mappings" : {
                                            "_doc" : {
                                                "properties" : {
                                                    "name": { "type" : "keyword" },
                                                    "data_index_name": { "type" : "keyword" },
                                                    "event_count": { "type" : "long" },
                                                    "oldest" : { "type" : "date" },
                                                    "lastest": { "type" : "date" }
                                                }
                                            }
                                        }
                                    })

        #create template for series data indices
        if not self.conn.indices.exists_template(self.series_template_name):
            idx_pattern = [ self.index_prefix + '*' ]
            body =  {
                "index_patterns" :  idx_pattern,
                "settings" : {
                    "index" : {
                        "sort.field" : "@timestamp", 
                        "sort.order" : "desc" 
                    }
                },
                "mappings": {
                    "_doc": {
                        "properties": {
                            "@timestamp": {
                                "type": "date"
                            },
                            "tag": {
                                "type": "keyword"
                            },
                            "context": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
            self.conn.indices.put_template(name=self.series_template_name, body=body )



    #---------------------------SEARCH------------------------------------------


    def getSeries(self, clientname, start='', end='', context='', tags='', interval='1H'):
        jsondata = []
        if self._findClientIndex(clientname):
            index_pattern = self.index_prefix + self.index_name + '-*'
            query = {
              "query": {
                "bool": {
                  "filter": []
                }
              },
              "aggs": {
                "my_aggregation": {
                  "date_histogram": {
                    "field":     "@timestamp",
                    "interval":  interval
                  }
                }
              }
            }

            if start or end:
                dict = {
                    "range": {
                        "@timestamp": {}
                    }
                }
                if start:
                    dict['range']['@timestamp']['gte'] = start
                if end:
                    dict['range']['@timestamp']['lte'] = end
                query['query']['bool']['filter'].append(dict)
                
            if tags:
                dict = {
                    "terms": {"tag": tags }
                }
                query['query']['bool']['filter'].append(dict)

            if context:
                dict = {
                    "terms": {"context": context }
                }
                query['query']['bool']['filter'].append(dict)

            response = self.conn.search(index=index_pattern, size=0, body=query)
            for element in response['aggregations']['my_aggregation']['buckets']:
                jsondata.append([element['key'], element['doc_count']])

        return jsondata


    def getClients(self):
        response = self.conn.search(index=self.client_index_name,
                        doc_type="_doc")
        jsondata = []
        if response:
            for element in response['hits']['hits']:
                client = {}
                client['name'] = element['_source'].get('name', '')
                client['count'] = element['_source'].get('event_count', '')
                client['start'] = element['_source'].get('oldest', '')
                client['end'] = element['_source'].get('latest', '')
                client['context'] = element['_source'].get('context', '')
                jsondata.append(client)
        return jsondata



    def getContexts(self, clientname):
        jsondata = [] 
        if self._findClientIndex(clientname):
            index_pattern = self.index_prefix + self.index_name + '-*'
            response = self.conn.search(index=index_pattern, 
                                        size=0, 
                                        body={
                                            "aggs": {
                                                "my_aggregation": {
                                                    "terms":  { 
                                                        "field" : "context",
                                                        "size": 10000
                                                    }
                                                }
                                            }
                                        })
            for element in response['aggregations']['my_aggregation']['buckets']:
                jsondata.append(element['key'])
        return jsondata


    def getTags(self, clientname):
        jsondata = []
        if self._findClientIndex(clientname):
            index_pattern = self.index_prefix + self.index_name + '-*'
            response = self.conn.search(index=index_pattern, 
                                        size=0, 
                                        body={
                                            "aggs": {
                                                "my_aggregation": {
                                                    "terms":  { 
                                                        "field" : "tag",
                                                        "size": 10000
                                                    }
                                                }
                                            }
                                        })
            for element in response['aggregations']['my_aggregation']['buckets']:
                jsondata.append(element['key'])
        return jsondata


    def _findClientIndex(self, clientname):
        index = ''
        response = self.conn.search(index = self.client_index_name,
                                     body = {
                                        "query": {
                                            "match": {
                                              "_id": clientname
                                            }
                                        }
                                    })
        if response['hits']['hits']:
            doc = response['hits']['hits'][0]
            index = doc['_source']['data_index_name']
        self.index_name = index
        return index


    #---------------------------INDEXING------------------------------------------

    #docspath is  the full path to the new client data files
    #todo: antes de crear nuevo cliente, fijarse si existe y borrarlo primero
    def addNewClient(self, clientname, indexname, docspath):
        self.index_name = self._cleanIndexName(indexname) if indexname else self._cleanIndexName(clientname)
        self._indexClientInfo(clientname)
        return self._indexSeriesData(docspath)   


    def _indexClientInfo(self, clientname):
        self.conn.index(index=self.client_index_name,
                    doc_type='_doc', 
                    body= {
                        "name": clientname,
                        "data_index_name": self.index_name,
                        "event_count": "0",
                    },
                    id=clientname)



    def _indexSeriesData(self, docspath):
        result = ''
        #self._createSeriesDataTemplate()
        self._createPipeline()
        files = [ f for f in os.listdir(docspath) if os.path.isfile(os.path.join(docspath,f)) ]
        for filename in files:
            with open(os.path.join(docspath,filename)) as f:
                data = json.load(f)
                result = bulk(self.conn, self._makeDocuments(data))
        return result



    #pipeline to automatically create monthly indices
    def _createPipeline(self):
        ic = IngestClient(self.conn)
        self.pipeline_id = 'monthlyprocessor'
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
        ic.put_pipeline(id=self.pipeline_id, body=pipeline_body)


    #generator to iterate over all documents and define doc structure
    def _makeDocuments(self, data):
        full_index_name = self.index_prefix + self.index_name
        for event in data:
            doc = {
                    '_index': full_index_name,
                    '_type': '_doc',
                    '_id': event['_id'],
                    'pipeline': self.pipeline_id,
                    '_source': {
                        '@timestamp': event['source']['date'], 
                        'tag': event['source']['tags'],
                        'context': event['source']['context']
                    }
            }
            yield(doc) 


    def _cleanIndexName(self, name):
        return name.strip(' _\n\t').lower().replace(" ", "")



    #---------------------------INDEX DELETING------------------------------------------

    def deleteClient(self, clientname):
        if self.conn.exists(index=self.client_index_name, doc_type='_doc', id=clientname):
            index = self._findClientIndex(clientname)
            full_index_name = self.index_prefix + index
            if index:
                if self.conn.indices.exists(full_index_name):
                    self.conn.indices.delete(full_index_name)
                pattern = self.index_prefix + self.index_name + '-*'
                self.conn.indices.delete(pattern)                
            self.conn.delete(index=self.client_index_name, doc_type='_doc', id=clientname)
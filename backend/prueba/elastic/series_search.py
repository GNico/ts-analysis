from elasticsearch.client import IndicesClient

from .es_connection import es


class SeriesSearch():

    def get_count(self, indexname):
        index_pattern = indexname + '-*'
        self.refresh(index_pattern)

        print('first count')
        print(index_pattern)
        response = es.count(index=index_pattern)

        print(response)
        return response['count']

    def refresh(self, indexname):
        ic = IndicesClient(es)
        res = ic.refresh(indexname)
        print(res)

    def get_series(self, indexname, start='', end='', context='', tags='', interval='1H'):
        requestedData = []        
        index_pattern = indexname + '-*'
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
                "terms": {"tag": [ tags ] }
            }
            query['query']['bool']['filter'].append(dict)

        if context:
            dict = {
                "terms": {"context": [ context ] }
            }
            query['query']['bool']['filter'].append(dict)

        response = es.search(index=index_pattern, size=0, body=query)
        for element in response['aggregations']['my_aggregation']['buckets']:
            requestedData.append([element['key'], element['doc_count']])

        return requestedData


    def get_contexts(self, indexname):
        requestedData = [] 
        index_pattern = indexname + '-*'
        response = es.search(index=index_pattern, 
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
            requestedData.append(element['key'])
        return requestedData


    def get_tags(self, indexname):
        requestedData = []
        index_pattern =  indexname + '-*'
        response = es.search(index=index_pattern, 
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
            requestedData.append(element['key'])
        return requestedData
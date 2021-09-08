from elasticsearch.client import IndicesClient
from .es_connection import es
import datetime

class SeriesSearch():
    def get_count(self, indexname):
        index_pattern = indexname + '-*'
        self.refresh(index_pattern)
        response = es.count(index=index_pattern)
        return response['count']

    def refresh(self, indexname):
        ic = IndicesClient(es)
        res = ic.refresh(indexname)

    #utc offset in minutes
    def get_series(self, indexname, start='', end='', context=[], tags=[], interval='1h', 
        filter_tags=False, filter_contexts=False, UTC_offset=0):
        index_pattern = indexname + '-*'
        query = self._build_series_query(start, end, context, tags, filter_tags, filter_contexts)
        query["aggs"] = {
            "interval_aggregation": {
              "date_histogram": {
                "field":     "@timestamp",
                "fixed_interval":  interval,
              }
            }
        }
        if UTC_offset:
            offset = '+' if UTC_offset > 0 else '-'
            offset += str(abs(UTC_offset)) + 'm'
            query["aggs"]["interval_aggregation"]["date_histogram"]["offset"] = offset     

        response = es.search(index=index_pattern, size=0, body=query)
        series_data = []    
        for element in response['aggregations']['interval_aggregation']['buckets']:
            series_data.append([element['key'], element['doc_count']])
        return series_data

    def get_series_range(self, indexname):
        index_pattern = indexname + '-*'
        query = self._build_series_query()
        query["aggs"] = {
            "max_val": { "max": { "field": "@timestamp" } },
            "min_val": { "min": { "field": "@timestamp" } }
        }
        response = es.search(index=index_pattern, size=0, body=query)
        min_val = response['aggregations']['min_val']['value_as_string']
        max_val = response['aggregations']['max_val']['value_as_string']
        return { 'start': min_val, 'end': max_val }


    def get_tags_count(self, indexname, start='', end='', context=[], tags=[], size=3, filter_tags=False, filter_contexts=False):
        index_pattern = indexname + '-*'
        query = self._build_series_query(start, end, context, tags, filter_tags, filter_contexts)
        total_docs = es.count(index=index_pattern, body=query)
        query["aggs"] = {
            "popular_tags": {
              "terms": {
                "field": "tag",
                "size": size
              }
            }
        }
        response = es.search(index=index_pattern, size=0, body=query)
        tags_count = []
        for element in response['aggregations']['popular_tags']['buckets']:
            tags_count.append({"tag": element['key'], "count": element['doc_count'] })
        return { "total": total_docs['count'], "tags_count": tags_count }


    def get_contexts(self, indexname):
        requestedData = [] 
        index_pattern = indexname + '-*'
        response = es.search(
            index=index_pattern, 
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
        response = es.search(
            index=index_pattern, 
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


    def get_last_events(self, indexname, start='', end='', context=[], tags=[], size=10):
        requestedData = []
        index_pattern = indexname + '-*'
        query = self._build_series_query(start, end, context, tags)
        query["sort"] = [{   
          "@timestamp": {
            "order": "desc"
          }
        }]   
        response = es.search(index=index_pattern, size=size, body=query)
        for element in response["hits"]["hits"]:
            requestedData.append([element['_source']['@timestamp'], element['_source']['tag']])
        return requestedData


    def _build_series_query(self, start='', end='', context=[], tags=[], filter_tags=False, filter_contexts=False):
        query = {
          "query": {
            "bool": {
              "filter": [],              
              "must": [],
              "must_not": []
            }
          },
        }
        if start or end:
            filter = {"range": {"@timestamp": {} }}
            if start:
                filter['range']['@timestamp']['gte'] = start
            if end:
                filter['range']['@timestamp']['lte'] = end
            query['query']['bool']['filter'].append(filter)     

        exists = {"exists": {"field": "tag"}}
        if filter_tags:
            if tags is None:
                #all docs with no empty tag field
                query['query']['bool']['must'].append(exists)
            elif tags:  
                #all docs with field in tags list
                filter = {"terms": {"tag.tree":  tags}}
                query['query']['bool']['filter'].append(filter)
            else:
                #all docs with empty tag field
                query['query']['bool']['must_not'].append(exists) 
        
        exists = {"exists": {"field": "context"}}
        if filter_contexts:
            if context is None:
                query['query']['bool']['must_not'].append(exists)                
            elif tags:  
                filter = {"terms": {"context":  context}}
                query['query']['bool']['filter'].append(filter)
            else:
                query['query']['bool']['must'].append(exists)

        return query
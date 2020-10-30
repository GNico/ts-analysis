from elasticsearch.client import IndicesClient

from .es_connection import es


class SeriesSearch():

    def get_count(self, indexname):
        index_pattern = indexname + '-*'
        self.refresh(index_pattern)
        response = es.count(index=index_pattern)
        return response['count']

    def refresh(self, indexname):
        ic = IndicesClient(es)
        res = ic.refresh(indexname)


    def get_series(self, indexname, start='', end='', context=[], tags=[], interval='1H'):
        index_pattern = indexname + '-*'
        query = self._build_series_query(start, end, context, tags)
        query["aggs"] = {
            "interval_aggregation": {
              "date_histogram": {
                "field":     "@timestamp",
                "interval":  interval
              }
            }
        }
        response = es.search(index=index_pattern, size=0, body=query)
        series_data = []
        for element in response['aggregations']['interval_aggregation']['buckets']:
            series_data.append([element['key'], element['doc_count']])
        return series_data


    def get_tags_count(self, indexname, start='', end='', context=[], tags=[], size=3):
        index_pattern = indexname + '-*'
        query = self._build_series_query(start, end, context, tags)
        total_docs = es.count(index=index_pattern, body=query)
        query["aggs"] = {
            "popular_tags": {
              "terms": {
                "field":    "tag",
                "size":     size
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


    def _build_series_query(self, start, end, context, tags):
        query = {
          "query": {
            "bool": {
              "filter": []
            }
          },
        }
        if start or end:
            dict = {"range": {"@timestamp": {} }}
            if start:
                dict['range']['@timestamp']['gte'] = start
            if end:
                dict['range']['@timestamp']['lte'] = end
            query['query']['bool']['filter'].append(dict)            
        if tags:
            dict = {"terms": {"tag.tree":  tags}}
            query['query']['bool']['filter'].append(dict)
        if context:
            dict = {"terms": {"context":  context}}
            query['query']['bool']['filter'].append(dict)
        return query
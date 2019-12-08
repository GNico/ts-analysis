from elasticsearch import Elasticsearch
#from django.conf import settings

#es = elasticsearch.Elasticsearch(settings.ELASTIC_SERVER, **settings.ELASTIC_CONFIG)
es = Elasticsearch(['localhost:9200'])


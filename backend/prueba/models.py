from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index_name = models.CharField(max_length=50)

    task_id = models.CharField(max_length=50)
    indexing = models.BooleanField(default=False)
    #doc_count = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)

    class Meta:        
        db_table = 'clients'

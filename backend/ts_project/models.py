from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index_name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default=None)
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:        
        db_table = 'clients'


class Analysis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    data_options = models.JSONField(default=dict)
    model = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'analysis'


class Pipeline(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    nodes = models.JSONField()
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'pipelines'
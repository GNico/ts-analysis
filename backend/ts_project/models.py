from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils import timezone
import json


class Client(models.Model):
    class Meta:        
        db_table = 'clients'

    name = models.CharField(max_length=50, unique=True)
    index_name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default=None)
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Analysis(models.Model):
    class Meta: 
        db_table = 'analysis'

    client = models.ForeignKey(Client, to_field='name', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    data_options = models.JSONField(default=dict)
    model = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)


class Pipeline(models.Model):
    class Meta: 
        db_table = 'pipelines'

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    nodes = models.JSONField()
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)


class PeriodicAnalysis(models.Model):    
    class Meta: 
        db_table = 'periodic_analysis'

    analysis = models.OneToOneField(Analysis, on_delete=models.CASCADE, primary_key=True)
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    time_interval = models.TextField(default='1h')
    created = models.DateTimeField(auto_now_add=True) 

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.analysis_id,
            task='periodictask',
            interval=self.interval_schedule,
            enabled=self.active,
            args=[self.analysis_id],
            start_time=timezone.now()
        )
        self.save()

    def update_task(self):
        self.task.enabled = self.active
        self.task.interval = self.interval_schedule
        self.task.save()

    @property
    def interval_schedule(self):
        import re
        number, letter = re.findall(r'[A-Za-z]+|\d+', self.time_interval)
        if letter == 's': 
            return IntervalSchedule.objects.get_or_create(every=number, period='seconds')[0]
        if letter == 'm': 
            return IntervalSchedule.objects.get_or_create(every=number, period='minutes')[0]
        if letter == 'h': 
            return IntervalSchedule.objects.get_or_create(every=number, period='hours')[0]
        if letter == 'd': 
            return IntervalSchedule.objects.get_or_create(every=number, period='days')[0]
        raise NotImplementedError(
            '''Interval Schedule for {interval} is invalid.'''.format(
                interval=self.time_interval.value))
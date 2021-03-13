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
    class Status(models.TextChoices):
        ACTIVE = 'active'
        DISABLED = 'disabled'

    class TimeInterval(models.TextChoices):
        ONE_MIN = '1 min'
        FIVE_MINS = '5 mins'
        ONE_HOUR = '1 hour'

    class Meta: 
        db_table = 'periodic_analysis'

    analysis = models.OneToOneField(Analysis, on_delete=models.CASCADE)
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)
    status = models.TextField(choices=Status.choices, default=Status.DISABLED)
    time_interval = models.TextField(choices=TimeInterval.choices, default=TimeInterval.ONE_MIN)
    created = models.DateTimeField(auto_now_add=True) 

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            task='periodictask',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.ONE_MIN:
            return IntervalSchedule.objects.get_or_create(every=1, period='minutes')
        if self.time_interval == TimeInterval.FIVE_MINS:
            return IntervalSchedule.objects.get_or_create(every=5, period='minutes')
        if self.time_interval == TimeInterval.ONE_HOUR:
            return IntervalSchedule.objects.get_or_create(every=1, period='hours')
        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))
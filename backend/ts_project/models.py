from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils import timezone

from . import task_priorities

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


class Monitor(models.Model):
    class Meta:
        db_table = 'monitors'

    name = models.TextField()

    def __str__(self):
        return self.name


class NotificationChannel(models.Model):
    class Meta:
        db_table = 'notification_channels'

    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name="notification_channels")
    email = models.EmailField(blank=False)
    

class PeriodicAnalysis(models.Model):    
    class Meta: 
        db_table = 'periodic_analysis'
        ordering = ['created']

    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name="detectors", null=True)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    alerts_enabled = models.BooleanField(default=False)
    time_interval = models.TextField(default='1h')
    relevant_period = models.TextField(default='1d')
    #data period o algo asi indepiendente del from to del analysis
    created = models.DateTimeField(auto_now_add=True)     
    last_run = models.DateTimeField(null=True)

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.id,
            task='periodic_analysis',
            interval=self.interval_schedule,
            enabled=self.active,
            args=[self.id],
            start_time=timezone.now(),
            priority=task_priorities.PERIODIC_ANALYSIS
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


class Results(models.Model):
    class Meta:
        db_table = 'results'

    periodic_analysis = models.ForeignKey(PeriodicAnalysis, on_delete=models.CASCADE, related_name="results")
    anomalies = models.JSONField()
    run_datetime = models.DateTimeField(null=True) 


class Incident(models.Model):
    class Meta:
        db_table = 'incidents'

    class State(models.TextChoices):
        OPEN = 'Open'
        CLOSED = 'Closed'

    periodic_analysis = models.ForeignKey(PeriodicAnalysis, on_delete=models.CASCADE, related_name="incidents")
    state = models.CharField(max_length=10, choices=State.choices, default=State.OPEN)
    start = models.DateTimeField() 
    end = models.DateTimeField() 
    score = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    desc = models.TextField(null=True)


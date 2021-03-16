from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import PeriodicAnalysis, Analysis

@receiver(post_save, sender=Analysis)
def create_periodic_analysis(sender, instance, created, **kwargs):
    if created:
        PeriodicAnalysis.objects.create(analysis=instance)


@receiver(pre_delete, sender=Analysis)
def delete_periodic_task(sender, instance, using, **kwargs):
    PeriodicAnalysis.objects.get(analysis=instance).delete()


@receiver(post_save, sender=PeriodicAnalysis)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.update_task()
      

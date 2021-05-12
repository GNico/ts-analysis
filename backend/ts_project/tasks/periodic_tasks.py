from celery import shared_task
from ..models import PeriodicAnalysis

@shared_task(bind=True, name="periodictask")
def periodictask(self, id):
    periodic_analysis = PeriodicAnalysis.objects.get(id=id)

    analysis_settings = periodic_analysis.analysis
    print(analysis_settings.data_options)

    print('''Running analysis with ID:  {analysis_id}, interval {interval} and relevant period {relevant}'''.format(
        analysis_id=periodic_analysis.analysis_id, interval=periodic_analysis.time_interval, relevant=periodic_analysis.relevant_period))
from celery import shared_task
from ..models import PeriodicAnalysis

@shared_task(bind=True, name="periodictask")
def periodictask(self, analysis_id):
    periodic_analysis = PeriodicAnalysis.objects.get(analysis_id=analysis_id)
    print("testing task")
    print('''Running analysis with ID:  {analysis_id}.'''.format(
        analysis_id=periodic_analysis.analysis_id))
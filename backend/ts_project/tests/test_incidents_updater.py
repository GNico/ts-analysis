#import unittest
from django.test import SimpleTestCase, TestCase
from ..models import Incident, PeriodicAnalysis, Analysis, Client
from datetime import datetime, timedelta
from ..tasks.incidents_updater import IncidentsComparator, IncidentsUpdater


class IncidentsComparatorTest(SimpleTestCase):
    def setUp(self):
        self.date_format = '%d/%m/%y %H:%M:%S'

    def test_comparator_soft_equal(self):
        start1 = datetime.strptime('18/09/19 00:00:00', self.date_format)
        inc1 = Incident(id=1, start=start1, end=start1 + timedelta(hours=1))
        inc2 = Incident(id=2, start=start1, end=start1 + timedelta(hours=2))
        self.assertTrue(IncidentsComparator.compare_soft(inc1, inc2))

    def test_comparator_soft_not_equal(self):
        start1 = datetime.strptime('18/09/19 00:00:00', self.date_format)
        inc1 = Incident(id=1, start=start1)
        inc2 = Incident(id=2, start=start1 + timedelta(hours=1))
        self.assertFalse(IncidentsComparator.compare_soft(inc1, inc2))

    def test_comparator_strict_equal(self):
        start1 = datetime.strptime('18/09/19 00:00:00', self.date_format)
        inc1 = Incident(id=1, start=start1, end=start1 + timedelta(hours=1))
        inc2 = Incident(id=2, start=start1, end=start1 + timedelta(hours=1))
        self.assertTrue(IncidentsComparator.compare_strict(inc1, inc2))

    def test_comparator_strict_not_equal(self):
        start1 = datetime.strptime('18/09/19 00:00:00', self.date_format)
        inc1 = Incident(id=1, start=start1, end=start1 + timedelta(hours=1))
        inc2 = Incident(id=2, start=start1, end=start1 + timedelta(hours=2))
        self.assertFalse(IncidentsComparator.compare_strict(inc1, inc2))


class IncidentsUpdaterTest(TestCase):
    def setUp(self):
        self.date_format = '%d/%m/%y %H:%M:%S' 
        start1 = datetime.strptime('18/09/19 00:00:00', self.date_format)  
        cl = Client.objects.create(id=1, name="pepe", status="ok")
        an = Analysis.objects.create(id=1, client=cl, name="pepe")
        pa = PeriodicAnalysis.objects.create(id=1, analysis=an)

        Incident.objects.create(id=1, periodic_analysis=pa, start=start1, end=start1 + timedelta(hours=1), state=Incident.State.OPEN)
        Incident.objects.create(id=2, periodic_analysis=pa, start=start1 + timedelta(hours=2), end=start1 + timedelta(hours=3), state=Incident.State.OPEN)



    def test_to_dict(self):
        model = Incident.objects.get(id=1)
        from django.forms.models import model_to_dict

      #  dictlist = [ model_to_dict(m) for m in models ]
        self.assertEqual(model.get('id'), 1)




       # self.assertEqual(dictinstance['state'], Incident.State.OPEN)

        # old = [ 
        #     Incident(id=1, start=start1, end=start1 + timedelta(hours=1), state=Incident.State.OPEN)
        #     Incident(id=2, start=start1 + timedelta(hours=5), end=start1 + timedelta(hours=6), state=Incident.State.OPEN)
        # ]
        # new = [
        #     Incident(id=3, start=start1, end=start1 + timedelta(hours=3), state=Incident.State.OPEN)
        #     Incident(id=4, start=start1 + timedelta(hours=6), end=start1 + timedelta(hours=8), state=Incident.State.OPEN)
        # ]
        
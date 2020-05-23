import unittest

from model import series_anomaly

class TestSeriesAnomaly(unittest.TestCase):

  def test_equality(self):
    a = series_anomaly.SeriesAnomaly(1, 2, 1.0)
    b = series_anomaly.SeriesAnomaly(1, 2, 1.0)
    self.assertEqual(a, b)
    self.assertEqual(hash(a), hash(b))

  def test_inequality(self):
    a = series_anomaly.SeriesAnomaly(1, 2, 1.0)
    b = series_anomaly.SeriesAnomaly(2, 3, 1.0)
    self.assertNotEqual(a, b)
    self.assertNotEqual(hash(a), hash(b))

  def test_set_elements(self):
    a1 = series_anomaly.SeriesAnomaly(1, 2, 1.0)
    a2 = series_anomaly.SeriesAnomaly(1, 2, 1.0)
    a3 = series_anomaly.SeriesAnomaly(2, 3, 1.0)
    a4 = series_anomaly.SeriesAnomaly(3, 4, 1.0)
    s = set([a1, a3])
    self.assertTrue(a1 in s)
    self.assertTrue(a2 in s)
    self.assertTrue(a3 in s)
    self.assertFalse(a4 in s)
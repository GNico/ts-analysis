import unittest

from model import anomaly


class TestAnomaly(unittest.TestCase):

    def test_equality(self):
        a = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        b = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_inequality(self):
        a = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        b = anomaly.Anomaly.from_epoch(2, 3, 1.0)
        self.assertNotEqual(a, b)
        self.assertNotEqual(hash(a), hash(b))

    def test_set_elements(self):
        a1 = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        a2 = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        a3 = anomaly.Anomaly.from_epoch(2, 3, 1.0)
        a4 = anomaly.Anomaly.from_epoch(3, 4, 1.0)
        s = set([a1, a3])
        self.assertTrue(a1 in s)
        self.assertTrue(a2 in s)
        self.assertTrue(a3 in s)
        self.assertFalse(a4 in s)

    def test_ordering(self):
        a1 = anomaly.Anomaly.from_epoch(1, 2, 1.0)
        a2 = anomaly.Anomaly.from_epoch(1, 3, 1.0)
        a3 = anomaly.Anomaly.from_epoch(3, 4, 1.0)
        a4 = anomaly.Anomaly.from_epoch(4, 5, 1.0)
        anomalies = [a3, a4, a2, a1]
        self.assertEqual([a1, a2, a3, a4], sorted(anomalies))

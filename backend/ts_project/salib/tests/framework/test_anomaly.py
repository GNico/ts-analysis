import unittest

from model.anomaly import Anomaly


class TestAnomaly(unittest.TestCase):

    def test_equality(self):
        a = Anomaly.from_epoch(1, 2, 1.0)
        b = Anomaly.from_epoch(1, 2, 1.0)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_inequality(self):
        a = Anomaly.from_epoch(1, 2, 1.0)
        b = Anomaly.from_epoch(2, 3, 1.0)
        self.assertNotEqual(a, b)
        self.assertNotEqual(hash(a), hash(b))

    def test_set_elements(self):
        a1 = Anomaly.from_epoch(1, 2, 1.0)
        a2 = Anomaly.from_epoch(1, 2, 1.0)
        a3 = Anomaly.from_epoch(2, 3, 1.0)
        a4 = Anomaly.from_epoch(3, 4, 1.0)
        s = set([a1, a3])
        self.assertTrue(a1 in s)
        self.assertTrue(a2 in s)
        self.assertTrue(a3 in s)
        self.assertFalse(a4 in s)

    def test_ordering(self):
        a1 = Anomaly.from_epoch(1, 2, 1.0)
        a2 = Anomaly.from_epoch(1, 3, 1.0)
        a3 = Anomaly.from_epoch(3, 4, 1.0)
        a4 = Anomaly.from_epoch(4, 5, 1.0)
        anomalies = [a3, a4, a2, a1]
        self.assertEqual([a1, a2, a3, a4], sorted(anomalies))

    def test_output_format(self):
        anomaly = Anomaly.from_epoch(1, 2, 1.0, 'awesome')
        anomaly.tag_algo('test_algo')
        expected = {
            'from': 1000,
            'to': 2000,
            'score': 1.0,
            'desc': 'awesome',
            'algo_id': 'test_algo'
        }
        self.assertEqual(expected, anomaly.output_format())

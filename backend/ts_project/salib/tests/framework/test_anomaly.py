import unittest

from model.anomaly import Anomaly
from model.series import Series
from model.pipeline.nodes.node import Node

class TestAnomaly(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.series = Series.from_array([
                        [0, 0],
                        [1, 1],
                        [2, 1],
                        [3, 0]],
                        1)

    def test_equality(self):
        a = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        b = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_inequality(self):
        a = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        b = Anomaly.from_epoch(self.series, 2, 3, 1.0)
        self.assertNotEqual(a, b)
        self.assertNotEqual(hash(a), hash(b))

    def test_set_elements(self):
        a1 = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        a2 = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        a3 = Anomaly.from_epoch(self.series, 2, 3, 1.0)
        a4 = Anomaly.from_epoch(self.series, 3, 4, 1.0)
        s = set([a1, a3])
        self.assertTrue(a1 in s)
        self.assertTrue(a2 in s)
        self.assertTrue(a3 in s)
        self.assertFalse(a4 in s)

    def test_ordering(self):
        a1 = Anomaly.from_epoch(self.series, 1, 2, 1.0)
        a2 = Anomaly.from_epoch(self.series, 1, 3, 1.0)
        a3 = Anomaly.from_epoch(self.series, 3, 4, 1.0)
        a4 = Anomaly.from_epoch(self.series, 4, 5, 1.0)
        anomalies = [a3, a4, a2, a1]
        self.assertEqual([a1, a2, a3, a4], sorted(anomalies))

    def test_output_format(self):
        anomaly = Anomaly.from_epoch(self.series, 1, 2, 1.0, 'awesome')
        anomaly.set_source_node(Node('test_node'))
        expected = {
            'from': 1000,
            'to': 2000,
            'score': 1.0,
            'desc': 'awesome',
            'source_node': 'test_node'
        }
        self.assertEqual(expected, anomaly.output_format())

    def test_epoch_span(self):
        anomaly = Anomaly.from_epoch(self.series, 1, 2, 1.0, 'awesome')
        self.assertEqual((1, 2), anomaly.epoch_span_secs())

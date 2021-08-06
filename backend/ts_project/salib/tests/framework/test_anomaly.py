import unittest
import numpy as np

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
                        [3, 0],
                        ])

    def test_copy(self):
        a = Anomaly.from_epoch(1, 2, 1.0)
        b = a.copy()
        self.assertEqual(a, b)
        self.assertEqual('132fe9c5a03d96f6b80b7484f87e3052', a.id())
        self.assertEqual(a.id(), b.id())

        b.set_source_anomalies([a])
        self.assertEqual('dd5ef91f83a839b68b8a456b01eb45fe', b.id())
        self.assertNotEqual(a.id(), b.id())
        self.assertNotEqual(a, b)

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
        all_ids = [
            'e4faf6ec4da15ed9a37f75d7bcc55d12',
            'cb1eda751f67ae1b5d0ae2bd69f20531',
            '5e1160651d9bf60d7136c193530e4c12',
            '9ab7768778c2eafba90943ca14e2b970',
            '0d78b95e849701520c5b38d7cbdecf58',
        ]
        self.assertEqual(len(all_ids), len(np.unique(all_ids)))
        self.output_format_case(1, 2, 1.0, 'test_node', [], {
            'id': all_ids.pop(),
            'from': 1000,
            'to': 2000,
            'score': 1.0,
            'source_anomalies': [],
            'source_node': 'test_node'
        })
        self.output_format_case(1, 1, 1.0, 'test_node', [], {
            'id': all_ids.pop(),
            'from': 1000,
            'to': 1000,
            'score': 1.0,
            'source_anomalies': [],
            'source_node': 'test_node'
        })
        self.output_format_case(1, 2, 0.0, 'test_node', [], {
            'id': all_ids.pop(),
            'from': 1000,
            'to': 2000,
            'score': 0.0,
            'source_anomalies': [],
            'source_node': 'test_node'
        })
        self.output_format_case(1, 2, 1.0, 'other_node', [], {
            'id': all_ids.pop(),
            'from': 1000,
            'to': 2000,
            'score': 1.0,
            'source_anomalies': [],
            'source_node': 'other_node'
        })
        source_anomaly = Anomaly.from_epoch(1, 2, 1.0)
        source_anomaly.set_source_node(Node('other_node'))
        self.output_format_case(1, 2, 1.0, 'test_node', [source_anomaly], {
            'id': all_ids.pop(),
            'from': 1000,
            'to': 2000,
            'score': 1.0,
            'source_anomalies': ['cb1eda751f67ae1b5d0ae2bd69f20531'],
            'source_node': 'test_node'
        })

    def output_format_case(self, start, end, score, source_node_id, source_anomalies, expected):
        anomaly = Anomaly.from_epoch(start, end, score)
        anomaly.set_source_node(Node(source_node_id))
        anomaly.set_source_anomalies(source_anomalies)
        self.assertEqual(expected, anomaly.output_format())

    def test_epoch_span(self):
        anomaly = Anomaly.from_epoch(1, 2, 1.0)
        self.assertEqual((1, 2), anomaly.epoch_span_secs())

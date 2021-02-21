import unittest

from model.anomaly import Anomaly
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.aggregators._or import Or

class TestOrAggregator(unittest.TestCase):

    def test_or_aggregator_edge_case(self):
        self.case([], [], [])

    def test_or_aggregator_base_case(self):
        series = None
        fst = [Anomaly.from_epoch(series, 0, 1, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = fst + snd
        self.case(fst, snd, expected)

    def case(self, fst_anomalies, snd_anomalies, expected_output):
        fst_input = NodeResult(None, None, anomalies=fst_anomalies)
        snd_input = NodeResult(None, None, anomalies=snd_anomalies)
        or_node = Or('test')
        result = or_node.execute([fst_input, snd_input])
        self.assertEqual(expected_output, result.anomalies)

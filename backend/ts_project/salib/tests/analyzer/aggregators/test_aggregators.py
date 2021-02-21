import unittest

from model.anomaly import Anomaly
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.aggregators._or import Or
from model.pipeline.nodes.aggregators._and import And


class TestAggregators(unittest.TestCase):

    def test_and_aggregator_no_overlap(self):
        and_node = And('test')
        and_node.set_param_value('full_overlap', False)
        series = None
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = []
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_some_overlap(self):
        and_node = And('test')
        and_node.set_param_value('full_overlap', False)
        series = None
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        expected = fst + snd
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_full_overlap(self):
        and_node = And('test')
        and_node.set_param_value('full_overlap', False)
        series = None
        a1 = Anomaly.from_epoch(series, 0, 5, 1.0)
        a2 = Anomaly.from_epoch(series, 2, 5, 1.0)
        a3 = Anomaly.from_epoch(series, 2, 6, 1.0)
        fst = [a1]
        snd = [a2, a3]
        expected = fst + snd
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_edge_case(self):
        self.case(And('test'), [], [], [])

    def test_or_aggregator_edge_case(self):
        self.case(Or('test'), [], [], [])

    def test_or_aggregator_base_case(self):
        series = None
        fst = [Anomaly.from_epoch(series, 0, 1, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = fst + snd
        self.case(Or('test'), fst, snd, expected)

    def case(self, node, fst_anomalies, snd_anomalies, expected_output):
        fst_input = NodeResult(None, None, anomalies=fst_anomalies)
        snd_input = NodeResult(None, None, anomalies=snd_anomalies)
        result = node.execute([fst_input, snd_input])
        self.assertEqual(expected_output, result.anomalies)

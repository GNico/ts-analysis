import unittest

from model.anomaly import Anomaly
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.node import Node
from model.pipeline.nodes.aggregators.union import Union
from model.pipeline.nodes.aggregators.intersect import Intersect


class TestAggregators(unittest.TestCase):

    def test_and_aggregator_no_overlap(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', True)
        series = None
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = []
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_some_overlap_strict(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', True)
        series = None
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        expected = []
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_some_overlap_non_strict(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', False)
        series = None
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2]
        self.case(and_node, [a1], [a2], expected)

    def test_and_aggregator_some_overlap_strict(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', True)
        series = None
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a3 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2]
        self.case(and_node, [a1], [a2, a3], expected)

    def test_and_aggregator_some_overlap_nonstrict(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', False)
        series = None
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a3 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2, a3]
        self.case(and_node, [a1], [a2, a3], expected)

    def test_and_aggregator_full_overlap(self):
        and_node = Intersect('test')
        and_node.set_param_value('strict', False)
        series = None
        a1 = Anomaly.from_epoch(series, 0, 5, 1.0)
        a2 = Anomaly.from_epoch(series, 2, 5, 1.0)
        a3 = Anomaly.from_epoch(series, 2, 6, 1.0)
        fst = [a1]
        snd = [a2, a3]
        expected = fst + snd
        self.case(and_node, fst, snd, expected)

    def test_and_aggregator_edge_case(self):
        self.case(Intersect('test'), [], [], [])

    def test_or_aggregator_edge_case(self):
        self.case(Union('test'), [], [], [])

    def test_or_aggregator_base_case(self):
        series = None
        fst = [Anomaly.from_epoch(series, 0, 1, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = fst + snd
        self.case(Union('test'), fst, snd, expected)

    def case(self, node, fst_anomalies, snd_anomalies, expected_output):
        self.maxDiff = None

        fst_node = Node('fst')
        snd_node = Node('snd')
        
        [a.set_source_node(fst_node) for a in fst_anomalies]
        [a.set_source_node(snd_node) for a in snd_anomalies]

        fst_input = NodeResult(None, None, anomalies=fst_anomalies)
        snd_input = NodeResult(None, None, anomalies=snd_anomalies)
        
        result = node.execute([fst_input, snd_input])
        
        self.assertEqual(set(expected_output), set(result.anomalies))

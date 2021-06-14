import unittest

from model.anomaly import Anomaly
from model.series import Series
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.node import Node
from model.pipeline.nodes.aggregators.union import Union
from model.pipeline.nodes.aggregators.intersect import Intersect

# Test series
series = Series.from_array([
    [0, 0],
    [1, 0],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 0]
], 1, 's')

class TestAggregators(unittest.TestCase):


    ## Temporal

    def test_intersect_aggregator_temporal_no_overlap(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = []
        self.case_temporal(intersect, fst, snd, expected)

    def test_intersect_aggregator_temporal_edge_case(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        self.case_temporal(intersect, [], [], [])

    def test_intersect_aggregator_temporal_some_overlap_pair_case1(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        expected = [(1, 2)]
        self.case_temporal(intersect, fst, snd, expected)

    def test_intersect_aggregator_temporal_some_overlap_pair_case2(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        fst = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        snd = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        expected = [(1, 2)]
        self.case_temporal(intersect, fst, snd, expected)

    def test_intersect_aggregator_temporal_some_overlap_pair_case3(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        fst = [Anomaly.from_epoch(series, 0, 4, 1.0)]
        snd = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        expected = [(1, 3)]
        self.case_temporal(intersect, fst, snd, expected)

    def test_intersect_aggregator_temporal_some_overlap_pair_case4(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'temporal')
        fst = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        snd = [Anomaly.from_epoch(series, 0, 4, 1.0)]
        expected = [(1, 3)]
        self.case_temporal(intersect, fst, snd, expected)

    ## Anomaly wise

    def test_intersect_aggregator_anomaly_wise_no_overlap(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', True)
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = []
        self.case_anomaly_wise(intersect, fst, snd, expected)

    def test_intersect_aggregator_anomaly_wise_some_overlap_strict(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', True)
        fst = [Anomaly.from_epoch(series, 0, 2, 1.0)]
        snd = [Anomaly.from_epoch(series, 1, 3, 1.0)]
        expected = []
        self.case_anomaly_wise(intersect, fst, snd, expected)

    def test_intersect_aggregator_anomaly_wise_some_overlap_non_strict(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', False)
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2]
        self.case_anomaly_wise(intersect, [a1], [a2], expected)

    def test_intersect_aggregator_anomaly_wise_some_overlap_strict_three(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', True)
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a3 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2]
        self.case_anomaly_wise(intersect, [a1], [a2, a3], expected)

    def test_intersect_aggregator_anomaly_wise_some_overlap_nonstrict_three(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', False)
        a1 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a2 = Anomaly.from_epoch(series, 0, 2, 1.0)
        a3 = Anomaly.from_epoch(series, 1, 3, 1.0)
        expected = [a1, a2, a3]
        self.case_anomaly_wise(intersect, [a1], [a2, a3], expected)

    def test_intersect_aggregator_anomaly_wise_full_overlap(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        intersect.set_param_value('strict', False)
        a1 = Anomaly.from_epoch(series, 0, 5, 1.0)
        a2 = Anomaly.from_epoch(series, 2, 5, 1.0)
        a3 = Anomaly.from_epoch(series, 2, 6, 1.0)
        fst = [a1]
        snd = [a2, a3]
        expected = fst + snd
        self.case_anomaly_wise(intersect, fst, snd, expected)

    def test_intersect_aggregator_anomaly_wise_edge_case(self):
        intersect = Intersect('test')
        intersect.set_param_value('resolution', 'anomaly')
        self.case_anomaly_wise(intersect, [], [], [])

    def test_union_aggregator_edge_case(self):
        self.case_anomaly_wise(Union('test'), [], [], [])

    def test_union_aggregator_base_case(self):
        fst = [Anomaly.from_epoch(series, 0, 1, 1.0)]
        snd = [Anomaly.from_epoch(series, 2, 4, 1.0)]
        expected = fst + snd
        self.case_anomaly_wise(Union('test'), fst, snd, expected)

    def case(self, node, fst_anomalies, snd_anomalies):
        self.maxDiff = None


        fst_node = Node('fst')
        snd_node = Node('snd')
        
        [a.set_source_node(fst_node) for a in fst_anomalies]
        [a.set_source_node(snd_node) for a in snd_anomalies]

        fst_series = Series.from_array([
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0]
        ], 1, 's')

        snd_series = Series.from_array([
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0]
        ], 1, 's')

        fst_input = NodeResult(None, None, output_series=fst_series, anomalies=fst_anomalies)
        snd_input = NodeResult(None, None, output_series=snd_series, anomalies=snd_anomalies)
        
        result = node.execute([fst_input, snd_input])

        expected_display_series = {'input_1': fst_series, 'input_2': snd_series}
        self.assertEqual(expected_display_series, result.display_series())
        return result.anomalies

    def case_anomaly_wise(self, node, fst_anomalies, snd_anomalies, expected_output):
        anomalies = self.case(node, fst_anomalies, snd_anomalies)
        self.assertEqual(set(expected_output), set(anomalies))

    def case_temporal(self, node, fst_anomalies, snd_anomalies, expected_output):
        anomalies = self.case(node, fst_anomalies, snd_anomalies)
        anomalies_epochs = list(map(lambda a: a.epoch_span_secs(), anomalies))
        self.assertEqual(set(expected_output), set(anomalies_epochs))

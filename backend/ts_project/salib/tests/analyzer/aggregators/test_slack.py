import unittest

from model.anomaly import Anomaly
from model.series import Series
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.node import Node
from model.pipeline.nodes.aggregators.slack import Slack

class TestSlack(unittest.TestCase):

    def test_slack(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', '25%')
        fst = [Anomaly.from_epoch(0, 2, 1.0)]
        snd = [Anomaly.from_epoch(2, 4, 1.0)]
        expected = []
        self.case_temporal(intersect, fst, snd, expected)

    def case(self, node, fst_anomalies, snd_anomalies):
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
        
        result = node.execute([fst_input, snd_input], False)

        expected_display_series = {'input_1': fst_series, 'input_2': snd_series}
        self.assertEqual(expected_display_series, result.display_series())
        return result.anomalies

    def case_temporal(self, node, fst_anomalies, snd_anomalies, expected_output):
        anomalies = self.case(node, fst_anomalies, snd_anomalies)
        anomalies_epochs = list(map(lambda a: a.epoch_span_secs(), anomalies))
        self.assertEqual(set(expected_output), set(anomalies_epochs))

import unittest

from model.anomaly import Anomaly
from model.series import Series
from model.pipeline.nodes.node_result import NodeResult
from model.pipeline.nodes.node import Node
from model.pipeline.nodes.aggregators.slack import Slack

class TestSlack(unittest.TestCase):

    def test_slack_single_anomaly_no_min(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 100)
        intersect.set_param_value('min_span', '')
        fst = [Anomaly.from_epoch(1, 3, 1.0)]
        snd = []
        expected_anomalies = [
            {
                'id': 'c386a8dcb491be05ee22d597a568c6c5',
                'from': 0,
                'to': 4000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4'],
                'source_node': 'test',
            }
        ]
        expected_debug = {}
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        fst = [Anomaly.from_epoch(1, 3, 1.0)]
        snd = []
        expected_anomalies = [
            {
                'id': 'c386a8dcb491be05ee22d597a568c6c5',
                'from': 0,
                'to': 4000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4'],
                'source_node': 'test',
            }
        ]
        expected_debug = {}
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine_same(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        fst = [Anomaly.from_epoch(1, 3, 1.0), Anomaly.from_epoch(3, 5, 1.0)]
        snd = []
        expected_anomalies = [
            {
                'id': 'c386a8dcb491be05ee22d597a568c6c5',
                'from': 0,
                'to': 7000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4','907118cc03fec0a8d2c575b1954afdc4'],
                'source_node': 'test',
            }
        ]
        expected_debug = {}
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_combine_test(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        fst = [Anomaly.from_epoch(1, 3, 1.0)]
        snd = []
        expected_anomalies = [
            {
                'id': '907118cc03fec0a8d2c575b1954afdc4',
                'from': 1000,
                'to': 3000,
                'score': 1.0,
                'source_anomalies': [],
                'source_node': 'fst',
            }
        ]
        expected_debug = {}
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def case(self, node, fst_anomalies, snd_anomalies, expected_output, expected_debug):
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
        
        result = node.execute([fst_input, snd_input], True)

        expected_display_series = {'input_1': fst_series, 'input_2': snd_series}
        self.assertEqual(expected_display_series, result.display_series())

        actual_anomalies = list(map(lambda a: a.output_format(), result.anomalies))
        self.assertEqual(expected_output, actual_anomalies)
        self.assertEqual(expected_debug, result.debug_info)

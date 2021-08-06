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
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3)]
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
        expected_debug = {
            'anomaly_count_diff': 0,
            'end_anomaly_count': 1,
            'start_anomaly_count': 1
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3)]
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
        expected_debug = {
            'anomaly_count_diff': 0,
            'end_anomaly_count': 1,
            'start_anomaly_count': 1
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine_same(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(3, 5)]
        snd = []
        expected_anomalies = [
            {
                'id': 'c3a73aa49c1e4c20b0fbed653cf17538',
                'from': 0,
                'to': 6000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4','1ee724e9a7a81b6036caa98a0928be3b'],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -1,
            'end_anomaly_count': 1,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine3_same(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(2, 4), Anomaly.from_epoch(3, 5)]
        snd = []
        expected_anomalies = [
            {
                'id': '6d23e36c49116cac5a689601aea01a4b',
                'from': 0,
                'to': 6000,
                'score': 1.0,
                'source_anomalies': [
                    '907118cc03fec0a8d2c575b1954afdc4',
                    'fae6500ecb59c1e6919c7ed915e3c9ea',
                    '1ee724e9a7a81b6036caa98a0928be3b'
                ],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -2,
            'end_anomaly_count': 1,
            'start_anomaly_count': 3
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine3_same_modify(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(2, 4), Anomaly.from_epoch(3, 5)]
        snd = []
        expected_anomalies = [
            {
                'id': '6ce5c127caf55b9c597b8a7df7253587',
                'from': 1000,
                'to': 5000,
                'score': 1.0,
                'source_anomalies': [
                    '907118cc03fec0a8d2c575b1954afdc4',
                    'fae6500ecb59c1e6919c7ed915e3c9ea',
                    '1ee724e9a7a81b6036caa98a0928be3b'
                ],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -2,
            'end_anomaly_count': 1,
            'start_anomaly_count': 3
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_combine2_min_gap_modify(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        intersect.set_param_value('min_gap', '2')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(3, 4)]
        snd = []
        expected_anomalies = [
            {
                'id': '4df66ed193a28317221ac37f78d0d7dc',
                'from': 1000,
                'to': 4000,
                'score': 1.0,
                'source_anomalies': [
                    '907118cc03fec0a8d2c575b1954afdc4',
                    '2258259e7e550cbe14d3f31b2172e150'
                ],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -1,
            'end_anomaly_count': 1,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_combine2_min_gap_no_modify(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        intersect.set_param_value('min_gap', '2')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(5, 7)]
        snd = []
        expected_anomalies = [
            {
                'id': '907118cc03fec0a8d2c575b1954afdc4',
                'from': 1000,
                'to': 3000,
                'score': 1.0,
                'source_anomalies': [],
                'source_node': 'fst',
            },
            {
                'id': '39b7611a1843441315cda0b35edd070a',
                'from': 5000,
                'to': 7000,
                'score': 1.0,
                'source_anomalies': [],
                'source_node': 'fst',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': 0,
            'end_anomaly_count': 2,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine_repeated_same_start_end(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(1, 3)]
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
        expected_debug = {
            'anomaly_count_diff': -1,
            'end_anomaly_count': 1,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine_repeated_same_end(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(2, 3)]
        snd = []
        expected_anomalies = [
            {
                'id': '38d8163446902c87895ce84636452da2',
                'from': 1000,
                'to': 3000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4','3c7002f0fd6171fa486fb34a853becac'],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -1,
            'end_anomaly_count': 1,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_combine_diff(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3)]
        snd = [Anomaly.from_epoch(3, 5)]
        expected_anomalies = [
            {
                'id': 'fdccae96bcc19b9b66343b183196a132',
                'from': 0,
                'to': 6000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4','00a3ef8b7bacb638bd304696a563e771'],
                'source_node': 'test',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': -1,
            'end_anomaly_count': 1,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_single_anomaly_min_span_does_not_combine(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '4')
        intersect.set_param_value('min_gap', '')
        fst = [Anomaly.from_epoch(1, 3), Anomaly.from_epoch(10, 20)]
        snd = []
        expected_anomalies = [
            {
                'id': 'c386a8dcb491be05ee22d597a568c6c5',
                'from': 0,
                'to': 4000,
                'score': 1.0,
                'source_anomalies': ['907118cc03fec0a8d2c575b1954afdc4'],
                'source_node': 'test',
            },
            {
                'id': '3548387b8640052ccbcfc8f0fb4438e3',
                'from': 10000,
                'to': 20000,
                'score': 1.0,
                'source_anomalies': [],
                'source_node': 'fst',
            }
        ]
        expected_debug = {
            'anomaly_count_diff': 0,
            'end_anomaly_count': 2,
            'start_anomaly_count': 2
        }
        self.case(intersect, fst, snd, expected_anomalies, expected_debug)

    def test_slack_edge_case_identity(self):
        intersect = Slack('test')
        intersect.set_param_value('slack', 0)
        intersect.set_param_value('min_span', '')
        fst = [Anomaly.from_epoch(1, 3)]
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
        expected_debug = {
            'anomaly_count_diff': 0,
            'end_anomaly_count': 1,
            'start_anomaly_count': 1
        }
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
        ])

        snd_series = Series.from_array([
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0]
        ])

        fst_input = NodeResult(None, None, output_series=fst_series, anomalies=fst_anomalies)
        snd_input = NodeResult(None, None, output_series=snd_series, anomalies=snd_anomalies)
        
        result = node.execute([fst_input, snd_input], True)

        expected_display_series = {'input_1': fst_series, 'input_2': snd_series}
        self.assertEqual(expected_display_series, result.display_series())

        actual_anomalies = list(map(lambda a: a.output_format(), result.anomalies))
        self.assertEqual(expected_output, actual_anomalies)
        self.assertEqual(expected_debug, result.debug_info)
        # Check no anomaly sources outside of original anomalies
        all_anomaly_sources = set()
        for anomaly in result.anomalies:
            for source_anomaly in anomaly.source_anomalies:
                all_anomaly_sources.add(source_anomaly)
        self.assertEqual(set(), all_anomaly_sources - set(fst_anomalies + snd_anomalies))

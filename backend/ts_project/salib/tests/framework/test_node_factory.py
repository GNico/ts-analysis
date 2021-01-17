import unittest

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):

    def test_aggregators_description(self):
        expected = [
            {
                'type': 'OR',
                'class': 'aggregator',
                'desc': 'Combine all anomalies from sources',
                'params': []
            },
            {
                'type': 'AND',
                'class': 'aggregator',
                'desc': 'Combine overlapping anomalies from sources',
                'params': []
            }
        ]
        self.maxDiff = None
        self.assertEqual(expected, NodeFactory.aggregators_description())

    def test_detectors_description(self):
        expected = [
            {
                'type': 'EMA',
                'class': 'detector',
                'desc': 'Exponential moving average',
                'params': [
                    {
                        'id': 'decay',
                        'max': 1,
                        'min': 0,
                        'type': 'BoundedFloat',
                        'value': 0.9,
                    },
                    {
                        'id': 'threshold',
                        'type': 'Float',
                        'value': 2,
                    }
                ]
            }
        ]
        self.maxDiff = None
        self.assertEqual(expected, NodeFactory.detectors_description())

    def test_parsing(self):
        builder = NodeFactory.detector('EMA')
        builder.set_param_value('decay', 0.95)
        builder.set_param_value('threshold', 1)
        ema = builder.build()

        obj = {
            'class': 'detector',
            'type': 'EMA',
            'params': [
                {
                    'id': 'decay',
                    'value': 0.95
                },
                {
                    'id': 'threshold',
                    'value': 1
                }
            ]
        }
        ema_from_json = NodeFactory.from_json(obj)

        self.assertEqual(ema.id(), ema_from_json.id())
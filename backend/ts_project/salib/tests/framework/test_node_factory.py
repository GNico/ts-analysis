import unittest

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):

    def test_aggregators_description(self):
        expected = [
            {
                'type': 'OR',
                'class': 'aggregator',
                'desc': 'Combine all anomalies from sources',
                'display': 'Or',
                'params': []
            },
            {
                'type': 'AND',
                'class': 'aggregator',
                'desc': 'Combine overlapping anomalies from sources',
                'display': 'And',
                'params': []
            }
        ]
        self.maxDiff = None
        self.assertEqual(expected, NodeFactory.aggregators_description())

    def test_detectors_description(self):
        expected = [
            {
                'type': 'EMA',
                'display': 'Exponential moving average',
                'desc': 'Exponential moving average with decay rate and minimum required threshold',
                'class': 'detector',
                'params': [
                    {
                        'id': 'decay',
                        'display': 'Decay',
                        'desc': 'Decay rate',
                        'max': 1,
                        'min': 0,
                        'type': 'BoundedFloat',
                        'value': 0.9,
                    },
                    {
                        'id': 'threshold',
                        'display': 'Deviations threshold',
                        'desc': 'Min required deviations threshold',
                        'type': 'Float',
                        'value': 2,
                    }
                ]
            }
        ]
        self.maxDiff = None
        self.assertEqual(expected, NodeFactory.detectors_description())

    def test_parsing(self):
        builder = NodeFactory.detector('test_id', 'EMA')
        builder.set_param_value('decay', 0.95)
        builder.set_param_value('threshold', 1)
        ema = builder.build()
        self.assertEqual(str(ema), 'EMA(0.95,1)[test_id]')

        obj = {
            'id': 'test_id',
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
        self.assertEqual(str(ema), str(ema_from_json))

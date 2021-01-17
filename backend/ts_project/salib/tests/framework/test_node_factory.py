import unittest

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):

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
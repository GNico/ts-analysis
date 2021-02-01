import unittest

from model.pipeline.pipeline import Pipeline


class TestPipeline(unittest.TestCase):

    def test_parsing_explicit_aggregator(self):
        obj = {
            'nodes': [
                {
                    'id': '1',
                    'group': 'aggregator',
                    'type': 'OR',
                    'params': [],
                    'sources': ['2', '3']
                },
                {
                    'id': '2',
                    'group': 'detector',
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
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'EMA',
                    'params': [
                        {
                            'id': 'decay',
                            'value': 0.9
                        },
                        {
                            'id': 'threshold',
                            'value': 2
                        }
                    ],
                    'sources': []
                }
            ]
        }
        pipeline = Pipeline.from_json(obj)

        self.assertEqual('_Root(1)', str(pipeline.root_node))
        self.assertEqual(1, len(pipeline.root_node.sources))
        orNode = pipeline.root_node.sources[0]
        self.assertEqual('OR(2,3)', str(orNode))
        self.assertEqual(2, len(orNode.sources))
        self.assertEqual('EMA(0.95,1)[2]', str(orNode.sources[0]))
        self.assertEqual('EMA(0.9,2)[3]', str(orNode.sources[1]))

    def test_parsing_implicit_aggregator(self):
        obj = {
            'nodes': [
                {
                    'id': '2',
                    'group': 'detector',
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
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'EMA',
                    'params': [
                        {
                            'id': 'decay',
                            'value': 0.9
                        },
                        {
                            'id': 'threshold',
                            'value': 2
                        }
                    ],
                    'sources': []
                }
            ]
        }
        pipeline = Pipeline.from_json(obj)

        self.assertEqual('_Root(2,3)', str(pipeline.root_node))
        self.assertEqual(2, len(pipeline.root_node.sources))
        self.assertEqual('EMA(0.95,1)[2]', str(pipeline.root_node.sources[0]))
        self.assertEqual('EMA(0.9,2)[3]', str(pipeline.root_node.sources[1]))
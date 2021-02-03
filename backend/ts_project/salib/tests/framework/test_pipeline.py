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
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': False
                        }
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'EMA',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
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
        self.assertEqual('SimpleThreshold(None,None,False)[2]', str(orNode.sources[0]))
        self.assertEqual('SimpleThreshold(None,None,True)[3]', str(orNode.sources[1]))

    def test_parsing_implicit_aggregator(self):
        obj = {
            'nodes': [
                {
                    'id': '2',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': False
                        }
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'EMA',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        }
                    ],
                    'sources': []
                }
            ]
        }
        pipeline = Pipeline.from_json(obj)

        self.assertEqual('_Root(2,3)', str(pipeline.root_node))
        self.assertEqual(2, len(pipeline.root_node.sources))
        self.assertEqual('SimpleThreshold(None,None,False)[2]', str(pipeline.root_node.sources[0]))
        self.assertEqual('SimpleThreshold(None,None,True)[3]', str(pipeline.root_node.sources[1]))
import unittest

from model.pipeline.pipeline import Pipeline


class TestPipeline(unittest.TestCase):

    def test_parsing(self):
        obj = {
            'nodes': [
                {
                    'id': '1',
                    'class': 'aggregator',
                    'type': 'OR',
                    'params': [],
                    'sources': ['2', '3']
                },
                {
                    'id': '2',
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
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'class': 'detector',
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

        self.assertEqual('OR(2,3)', str(pipeline.root_node))
        self.assertEqual(2, len(pipeline.root_node.sources))
        self.assertEqual('EMA(0.95,1)[2]', str(pipeline.root_node.sources[0]))
        self.assertEqual('EMA(0.9,2)[3]', str(pipeline.root_node.sources[1]))
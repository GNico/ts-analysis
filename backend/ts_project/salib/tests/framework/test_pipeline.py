import unittest

from model.pipeline.pipeline import Pipeline


class TestPipeline(unittest.TestCase):

    def test_parsing_explicit_aggregator(self):
        obj = {
            'nodes': [
                {
                    'id': '1',
                    'group': 'aggregator',
                    'type': 'Union',
                    'params': [],
                    'sources': [
                        {
                            'type': 'node',
                            'ref':'2',
                        },
                        {
                            'type': 'node',
                            'ref':'3',
                        },
                    ]
                },
                {
                    'id': '2',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': False
                        },
                        {
                            'id': 'strict',
                            'value': False
                        }
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        },
                        {
                            'id': 'strict',
                            'value': False
                        }
                    ],
                    'sources': []
                }
            ]
        }
        
        pipeline = Pipeline.from_json(obj)

        self.assertEqual('_Root(Node[1])', str(pipeline.root_node))
        self.assertEqual(1, len(pipeline.root_node.sources))
        or_node = pipeline.resolve_node_reference(pipeline.root_node.sources[0].ref)
        self.assertEqual('Union(Node[2],Node[3])', str(or_node))
        self.assertEqual(2, len(or_node.sources))
        self.assertEqual('Node[2]', str(or_node.sources[0]))
        self.assertEqual('Node[3]', str(or_node.sources[1]))
        or_node_source_0_resolved = pipeline.resolve_node_reference(or_node.sources[0].ref)
        or_node_source_1_resolved = pipeline.resolve_node_reference(or_node.sources[1].ref)
        self.assertEqual('SimpleThreshold(None,None,False,False)[2]', str(or_node_source_0_resolved))
        self.assertEqual('SimpleThreshold(None,None,True,False)[3]', str(or_node_source_1_resolved))

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
                        },
                        {
                            'id': 'strict',
                            'value': False
                        }
                    ],
                    'sources': []
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        },
                        {
                            'id': 'strict',
                            'value': True
                        }
                    ],
                    'sources': []
                }
            ]
        }
        pipeline = Pipeline.from_json(obj)

        self.assertEqual('_Root(Node[2],Node[3])', str(pipeline.root_node))
        self.assertEqual(2, len(pipeline.root_node.sources))
        self.assertEqual('Node[2]', str(pipeline.root_node.sources[0]))
        self.assertEqual('Node[3]', str(pipeline.root_node.sources[1]))

    def test_parsing_loop_detection_2nodes(self):
        obj = {
            'nodes': [
                {
                    'id': '1',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',

                            'value': False
                        },
                        {
                            'id': 'strict',
                            'value': False
                        }
                    ],
                    'sources': [
                        {
                            'type': 'node',
                            'ref': '2'
                        }
                    ]
                },
                {
                    'id': '2',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        },
                        {
                            'id': 'strict',
                            'value': True
                        }
                    ],
                    'sources': [
                        {
                            'type': 'node',
                            'ref': '1'
                        }
                    ]
                }
            ]
        }

        try:
            pipeline = Pipeline.from_json(obj)
            raise AssertionError("Should throw loop exception")
        except ValueError as e:
            self.assertEqual("Found recursion in node 1, path: ['1', '2']", str(e))

    def test_parsing_loop_detection_3nodes(self):
        obj = {
            'nodes': [
                {
                    'id': '1',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',

                            'value': False
                        },
                        {
                            'id': 'strict',
                            'value': False
                        }
                    ],
                    'sources': [
                        {
                            'type': 'node',
                            'ref': '2'
                        }
                    ]
                },
                {
                    'id': '2',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        },
                        {
                            'id': 'strict',
                            'value': True
                        }
                    ],
                    'sources': [
                        {
                            'type': 'node',
                            'ref': '3'
                        }
                    ]
                },
                {
                    'id': '3',
                    'group': 'detector',
                    'type': 'SimpleThreshold',
                    'params': [
                        {
                            'id': 'inside',
                            'value': True
                        },
                        {
                            'id': 'strict',
                            'value': True
                        }
                    ],
                    'sources': [
                        {
                            'type': 'node',
                            'ref': '1'
                        }
                    ]
                }
            ]
        }

        try:
            pipeline = Pipeline.from_json(obj)
            raise AssertionError("Should throw loop exception")
        except ValueError as e:
            self.assertEqual("Found recursion in node 1, path: ['1', '2', '3']", str(e))

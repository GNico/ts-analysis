import unittest

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):

    def test_node_list(self):
        self.maxDiff = None
        expected = {
            'transformer': [
                'StdNormalize',
                'EMA',
                'RollingAggregate'
            ],
            'detector': [
                'SimpleThreshold'
            ],
            'aggregator': [
                'OR',
                'AND'
            ]
        }
        self.assertEqual(expected, NodeFactory.nodes_list())

    def test_transformers_description(self):
        self.maxDiff = None
        expected = {
            'type': 'StdNormalize',
            'group': 'transformer',
            'display': 'Standard normalization',
            'desc': 'Normalize data such that mean = 0 and std dev = 1',
            'params': []
        }
        self.assertEqual(expected, NodeFactory.node_description('transformer', 'StdNormalize'))
        
        expected = {
            'type': 'EMA',
            'display': 'Exponential moving average',
            'desc': 'Exponential moving average with decay rate',
            'group': 'transformer',
            'params': [
                {
                    'id': 'decay',
                    'display': 'Decay',
                    'desc': 'Decay rate',
                    'max': 1,
                    'min': 0,
                    'type': 'BoundedFloat',
                    'conditions': [],
                    'value': 0.9
                }
            ]
        }
        self.assertEqual(expected, NodeFactory.node_description('transformer', 'EMA'))
        
        expected = {
            'type': 'RollingAggregate',
            'display': 'Rolling Aggregate',
            'desc': 'Rolling aggregate',
            'group': 'transformer',
            'params': [
                {
                    'id': 'window',
                    'type': 'String',
                    'display': 'Window',
                    'desc': 'Window size in time interval (eg: 1h)',
                    'conditions': [],
                    'value': '30m'
                },
                {
                    'id': 'center',
                    'type': 'Boolean',
                    'display': 'Center',
                    'desc': 'Center aggregation window around value',
                    'conditions': [],
                    'value': False
                },
                {
                    'id': 'min_periods',
                    'type': 'BoundedInt',
                    'display': 'Min. periods',
                    'desc': 'Min number of periods',
                    'value': None,
                    'conditions': [],
                    'min': 0,
                    'max': None,
                },
                {
                    'id': 'agg_method',
                    'type': 'Select',
                    'display': 'Aggregation',
                    'desc': 'Aggregation method',
                    'options': [
                        {'code': 'mean', 'display': 'Mean'},
                        {'code': 'median', 'display': 'Median'},
                        {'code': 'sum', 'display': 'Sum'},
                        {'code': 'min', 'display': 'Min'},
                        {'code': 'max', 'display': 'Max'},
                        {'code': 'quantile', 'display': 'Quantile'},
                        {'code': 'iqr', 'display': 'Inter-quartile range'},
                        {'code': 'idr', 'display': 'Inter-decile range'},
                        {'code': 'count', 'display': 'Value count'},
                        {'code': 'nnz', 'display': 'Non zero count'},
                        {'code': 'nunique', 'display': 'Unique count'},
                        {'code': 'std', 'display': 'Sample standard dev.'},
                        {'code': 'var', 'display': 'Sample variance'},
                        {'code': 'skew', 'display': 'Sample skewness'},
                        {'code': 'kurt', 'display': 'Sample kurtosis'}
                    ],
                    'value': 'mean',
                    'conditions': [],
                }
            ]
        }
        self.assertEqual(expected, NodeFactory.node_description('transformer', 'RollingAggregate'))

    def test_aggregators_description(self):
        self.maxDiff = None
        
        expected = {
            'type': 'OR',
            'group': 'aggregator',
            'desc': 'Combine all anomalies from sources',
            'display': 'Or',
            'params': []
        }
        self.assertEqual(expected, NodeFactory.node_description('aggregator', 'OR'))
        
        expected = {
            'type': 'AND',
            'group': 'aggregator',
            'desc': 'Combine overlapping anomalies from sources',
            'display': 'And',
            'params': []
        }
        self.assertEqual(expected, NodeFactory.node_description('aggregator', 'AND'))

    def test_detectors_description(self):
        self.maxDiff = None
        expected = {
            'type': 'SimpleThreshold',
            'display': 'Simple Threshold',
            'desc': 'Detect values outside of bounds',
            'group': 'detector',
            'params': [
                {
                    'id': 'inside',
                    'display': 'Inside',
                    'desc': 'If true, value must be within bounds',
                    'type': 'Boolean',
                    'conditions': [],
                    'value': False,
                },
                {
                    'id': 'strict',
                    'display': 'Strict',
                    'desc': 'Strict comparison on bounds',
                    'type': 'Boolean',
                    'conditions': [],
                    'value': False,
                },
                {
                    'id': 'lower',
                    'display': 'Lower',
                    'desc': 'Lower bound',
                    'type': 'Float',
                    'conditions': [],
                    'value': None,
                },
                {
                    'id': 'upper',
                    'display': 'Upper',
                    'desc': 'Upper bound',
                    'type': 'Float',
                    'conditions': [],
                    'value': None,
                }
            ]
        }
        self.assertEqual(expected, NodeFactory.node_description('detector', 'SimpleThreshold'))

    def test_parsing(self):
        builder = NodeFactory.detector('test_id', 'SimpleThreshold')
        builder.set_param_value('inside', False)
        builder.set_param_value('strict', False)
        builder.set_param_value('lower', 1)
        builder.set_param_value('upper', None)
        threshold = builder.build()
        self.assertEqual(str(threshold), 'SimpleThreshold(1,None,False,False)[test_id]')

        obj = {
            'id': 'test_id',
            'group': 'detector',
            'type': 'SimpleThreshold',
            'params': [
                {
                    'id': 'lower',
                    'value': 1
                },
                {
                    'id': 'inside',
                    'value': False
                },
                {
                    'id': 'strict',
                    'value': False
                }
            ]
        }
        th_from_json = NodeFactory.from_json(obj)
        self.assertEqual(str(threshold), str(th_from_json))

import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.node_source import InputRef
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

class TestDropout(unittest.TestCase):

    def test_dropout_mean_sub(self):
        factory = NodeFactory.transformer('test', 'Dropout')
        factory.set_param_value('context_window', 4)
        factory.set_param_value('dropout_window', 2)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', None)
        factory.set_param_value('agg_method', 'mean')
        factory.set_param_value('combine_method', 'sub')
        factory.set_param_value('combine_method_order', 'context-dropout')
        factory.add_source(InputRef('input'))
        ram = factory.build()

        self.case(ram, [-1, -2, 0, 2, 1])

    def test_dropout_centered_mean_sub(self):
        factory = NodeFactory.transformer('test', 'Dropout')
        factory.set_param_value('context_window', 4)
        factory.set_param_value('dropout_window', 2)
        factory.set_param_value('center', True)
        factory.set_param_value('min_periods', None)
        factory.set_param_value('agg_method', 'mean')
        factory.set_param_value('combine_method', 'sub')
        factory.set_param_value('combine_method_order', 'context-dropout')
        factory.add_source(InputRef('input'))
        ram = factory.build()

        self.case(ram, [1, 0, -2, 0, 1])

    def test_dropout_mean_prop(self):
        factory = NodeFactory.transformer('test', 'Dropout')
        factory.set_param_value('context_window', 2)
        factory.set_param_value('dropout_window', 1)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', None)
        factory.set_param_value('agg_method', 'mean')
        factory.set_param_value('combine_method', 'prop')
        factory.set_param_value('combine_method_order', 'dropout-context')
        factory.add_source(InputRef('input'))
        ram = factory.build()
        self.case(ram, [1, 1, 3, 1, 1/3, 1, 1])

    def test_dropout_centered_mean_prop(self):
        factory = NodeFactory.transformer('test', 'Dropout')
        factory.set_param_value('context_window', 3)
        factory.set_param_value('dropout_window', 1)
        factory.set_param_value('center', True)
        factory.set_param_value('min_periods', None)
        factory.set_param_value('agg_method', 'mean')
        factory.set_param_value('combine_method', 'prop')
        factory.set_param_value('combine_method_order', 'dropout-context')
        factory.add_source(InputRef('input'))
        ram = factory.build()
        # [1,1,1,3,3,1,1,1]
        self.case(ram, [1, 1/2, 3/2, 3/2, 1/2, 1])

    def case(self, node, expected_series):
        series = self.build_series()
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'input':series})
        result = analysis.result_for_node(node.id)

        self.assertEqual(expected_series, result.output_series.as_list())

    def build_series(self):
        series = Series.from_array([
            [0, 1],
            [1, 1],
            [2, 1],
            [3, 3],
            [4, 3],
            [5, 1],
            [6, 1],
            [7, 1],
        ])
        return series

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

class TestMultiRollingAggregate(unittest.TestCase):

    def test_multi_rolling_aggregate_proportion(self):
        factory = NodeFactory.transformer('test', 'MultiRollingAggregate')
        factory.set_param_value('window', 1)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'proportion')
        factory.add_source(InputRef('lhs'))
        factory.add_source(InputRef('rhs'))
        ram = factory.build()

        s1 = Series.from_array([[0, 1], [1, 2], [2, 3], [3, 4]], 1)
        s2 = Series.from_array([[0, 5], [1, 5], [2, 5], [3, 5]], 1)
        self.case(ram, s1, s2, list(s1.pdseries.index), [0.2, 0.4, 0.6, 0.8])

    def test_multi_rolling_aggregate_proportion_window(self):
        factory = NodeFactory.transformer('test', 'MultiRollingAggregate')
        factory.set_param_value('window', 2)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'proportion')
        factory.add_source(InputRef('lhs'))
        factory.add_source(InputRef('rhs'))
        ram = factory.build()

        s1 = Series.from_array([[0, 1], [1, 2], [2, 3], [3, 4]], 1)
        s2 = Series.from_array([[0, 5], [1, 5], [2, 5], [3, 5]], 1)
        self.case(ram, s1, s2, list(s1.pdseries.index), [0.2, 0.3, 0.5, 0.7])

    def test_multi_rolling_aggregate_correlation(self):
        factory = NodeFactory.transformer('test', 'MultiRollingAggregate')
        factory.set_param_value('window', 2)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'correlation_pearson')
        factory.add_source(InputRef('lhs'))
        factory.add_source(InputRef('rhs'))
        ram = factory.build()

        s1 = Series.from_array([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]], 1)
        s2 = Series.from_array([[0, 1], [1, 2], [2, 3], [3, 2], [4, 1]], 1)
        self.case(ram, s1, s2, list(s1.pdseries.index)[1:], [
            0.9999999999999999,
            0.9999999999999999,
            -0.9999999999999999,
            -0.9999999999999999,
        ])

    def case(self, node, s1, s2, expected_index, expected_series):
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'lhs':s1, 'rhs':s2})
        result = analysis.result_for_node(node.id)
        output_series = result.output_series

        self.assertEqual(expected_series, output_series.as_list())
        self.assertEqual(expected_index, list(output_series.pdseries.index))

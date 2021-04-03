import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.params.float import Float, BoundedFloat
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

from model.utils import timestamp_to_epoch

class TestDoubleRollingAggregate(unittest.TestCase):

    def test_double_rolling_aggregate_mean(self):
        series = self.build_triangle()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], series.as_list())
        
        factory = NodeFactory.transformer('test', 'DoubleRollingAggregate')
        factory.set_param_value('center', False)
        factory.set_param_value('diff', 'rel_diff')

        factory.set_param_value('window_rhs', '1s')
        factory.set_param_value('min_periods_rhs', 0)
        factory.set_param_value('agg_method_rhs', 'mean')

        factory.set_param_value('window_lhs', '2s')
        factory.set_param_value('min_periods_lhs', 0)
        factory.set_param_value('agg_method_lhs', 'mean')
        dra = factory.build()

        self.case(series, dra, [3.0, 1.0, 0.6, 0.42857142857142855, 0.3333333333333333, 0.2727272727272727, 0.23076923076923078, 0.2, 0.058823529411764705, -0.1111111111111111, -0.17647058823529413, -0.2, -0.23076923076923078, -0.2727272727272727, -0.3333333333333333, -0.42857142857142855, -0.6, -1.0])

    def case(self, series, node, expected_series):
        pipeline = Pipeline(node)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)
        result = analysis.result_for_node(node.id)
        self.assertEqual(expected_series, result.series.as_list())

    def build_triangle(self):
        sb_up = TestSeriesBuilder.linear(10, 0, 1)
        sb_down = TestSeriesBuilder.linear(10, 0, -1)
        sb_up.append(sb_down, True)
        series = sb_up.build()

        raw_values = series.as_list()
        self.assertEqual(2, raw_values.count(0))
        self.assertEqual(0, min(raw_values))
        self.assertEqual(0, raw_values[0])
        self.assertEqual(0, raw_values[-1])
        self.assertEqual(9, raw_values[10])
        self.assertEqual(9, max(raw_values))
        self.assertEqual(2, raw_values.count(9))
        return series

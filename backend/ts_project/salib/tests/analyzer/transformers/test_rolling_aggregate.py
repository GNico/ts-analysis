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

class TestRollingAggregate(unittest.TestCase):

    def test_rolling_aggregate_mean(self):
        series = self.build_triangle()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], series.as_list())
        
        factory = NodeFactory.transformer('test', 'RollingAggregate')
        factory.set_param_value('window', 2)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'mean')
        ram = factory.build()

        self.case(series, ram, [0.0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.0, 8.5, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5, 0.5])

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

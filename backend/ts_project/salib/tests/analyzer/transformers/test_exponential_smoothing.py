import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.node_source import InputRef
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

class TestExponentialSmoothing(unittest.TestCase):

    def test_exponential_smoothing_mean(self):
        
        factory = NodeFactory.transformer('test', 'ExponentialSmoothing')
        factory.set_param_value('span', '4')
        factory.set_param_value('min_periods', '')
        factory.set_param_value('recursive', False)
        factory.set_param_value('agg_method', 'mean')
        factory.add_source(InputRef('input'))
        ewma = factory.build()
        expected_debug_info = {
            'alpha': 0.4
        }
        self.case(ewma, [2.095, 2.487, 2.283, 1.755, 1.041], expected_debug_info)

    def case(self, node, expected_series, debug_info):
        series = self.build_triangle()
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'input':series})
        result = analysis.result_for_node(node.id)
        self.assertEqual(result.debug_info, debug_info)
        actual_series = result.output_series.as_list()
        for i in range(0, len(expected_series)):
            self.assertAlmostEqual(expected_series[i], actual_series[i], 2)

    def build_triangle(self):
        sb_up = TestSeriesBuilder.linear(4, 0, 1)
        sb_down = TestSeriesBuilder.linear(4, 0, -1)
        sb_up.append(sb_down, True)
        series = sb_up.build()

        raw_values = series.as_list()
        self.assertEqual([0, 1, 2, 3, 3, 2, 1, 0], raw_values)
        return series

import json
import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase
from model.pipeline.nodes.node_source import InputRef

from model.utils import timestamp_to_epoch

class TestFFTFilter(unittest.TestCase):

    def test_fft_filter(self):
        series = self.build_triangle()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], series.as_list())
        
        factory = NodeFactory.transformer('fft_filter', 'FFTFilter')
        factory.set_param_value('cutoff', 50)
        factory.set_param_value('output', 'resid')
        factory.add_source(InputRef('input'))
        fft_filter = factory.build()

        self.case(series, fft_filter, 
            [
              0.002508563093691407,
              0.9927198663527221,
              2.0113390739957944,
              2.9857119332223716,
              4.015838444032453,
              4.984161555967546,
              6.014288066777628,
              6.988660926004205,
              8.00728013364728,
              8.997491436906309,
              8.99749143690631,
              8.007280133647278,
              6.988660926004206,
              6.014288066777628,
              4.984161555967547,
              4.015838444032454,
              2.985711933222371,
              2.0113390739957935,
              0.9927198663527218,
              0.002508563093691407
            ])

    def case(self, series, node, expected_series):
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=True)
        inputs = {
            'input': series
        }
        analysis = analyzer.analyze(inputs)
        result = analysis.result_for_node(node.id)

        self.assertEqual(expected_series, result.output_series.as_list())

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

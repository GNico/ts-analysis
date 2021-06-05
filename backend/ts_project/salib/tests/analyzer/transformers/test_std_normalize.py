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

class TestStdNormalize(unittest.TestCase):

    def test_std_normalize(self):
        series = self.build_triangle()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], series.as_list())
        
        factory = NodeFactory.transformer('std_normalize', 'StdNormalize')
        factory.add_source(InputRef('input'))
        stdnormalize = factory.build()

        self.case(series, stdnormalize, 
            [-1.5270292013639366,
            -1.1876893788386174,
            -0.8483495563132981,
            -0.5090097337879789,
            -0.16966991126265962,
            0.16966991126265962,
            0.5090097337879789,
            0.8483495563132981,
            1.1876893788386174,
            1.5270292013639366,
            1.5270292013639366,
            1.1876893788386174,
            0.8483495563132981,
            0.5090097337879789,
            0.16966991126265962,
            -0.16966991126265962,
            -0.5090097337879789,
            -0.8483495563132981,
            -1.1876893788386174,
            -1.5270292013639366])

    def case(self, series, node, expected_series):
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        inputs = {
            'input': series
        }
        analysis = analyzer.analyze(inputs)
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

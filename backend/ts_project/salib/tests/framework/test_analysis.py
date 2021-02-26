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

class TestAnalysis(unittest.TestCase):

    def test_analysis_with_debug(self):
        self.maxDiff = None
        series = self.build_triangle()
       
        factory = NodeFactory.transformer('test_node', 'RollingAggregate')
        factory.set_param_value('window', 5)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'max')
        node = factory.build()

        pipeline = Pipeline(node)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)

        expected = {
            "anomalies": [],
            "debug_nodes": {
                "test_node": {
                    "anomalies": [],
                    "series": [
                        [0, 0],
                        [1000, 1],
                        [2000, 2],
                        [3000, 3],
                        [4000, 4],
                        [5000, 5],
                        [6000, 6],
                        [7000, 7],
                        [8000, 8],
                        [9000, 9],
                        [10000, 9],
                        [11000, 9],
                        [12000, 9],
                        [13000, 9],
                        [14000, 9],
                        [15000, 8],
                        [16000, 7],
                        [17000, 6],
                        [18000, 5],
                        [19000, 4],
                    ],
                }
            },
            "series": [
                [0, 0],
                [1000, 1],
                [2000, 2],
                [3000, 3],
                [4000, 4],
                [5000, 5],
                [6000, 6],
                [7000, 7],
                [8000, 8],
                [9000, 9],
                [10000, 9],
                [11000, 8],
                [12000, 7],
                [13000, 6],
                [14000, 5],
                [15000, 4],
                [16000, 3],
                [17000, 2],
                [18000, 1],
                [19000, 0],
            ],
        }

        self.assertEqual(expected, analysis.output_format())

    def test_analysis_without_debug(self):
        self.maxDiff = None
        series = self.build_triangle()
       
        factory = NodeFactory.transformer('test_node', 'RollingAggregate')
        factory.set_param_value('window', 5)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', 0)
        factory.set_param_value('agg_method', 'max')
        factory.set_debug(False)
        node = factory.build()

        pipeline = Pipeline(node)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)

        expected = {
            "anomalies": [],
            "debug_nodes": {},
            "series": [
                [0, 0],
                [1000, 1],
                [2000, 2],
                [3000, 3],
                [4000, 4],
                [5000, 5],
                [6000, 6],
                [7000, 7],
                [8000, 8],
                [9000, 9],
                [10000, 9],
                [11000, 8],
                [12000, 7],
                [13000, 6],
                [14000, 5],
                [15000, 4],
                [16000, 3],
                [17000, 2],
                [18000, 1],
                [19000, 0],
            ],
        }

        self.assertEqual(expected, analysis.output_format())

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

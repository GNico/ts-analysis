import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.node_source import InputRef
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
        factory.add_source(InputRef('input'))
        node = factory.build()

        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=True)
        analysis = analyzer.analyze({'input':series})

        expected = {
            "anomalies": [],
            "debug_nodes": {
                "test_node": {
                    "anomalies": [],
                    "series": {
                        "output": [
                            [0, 0.0],
                            [1000, 1.0],
                            [2000, 2.0],
                            [3000, 3.0],
                            [4000, 4.0],
                            [5000, 5.0],
                            [6000, 6.0],
                            [7000, 7.0],
                            [8000, 8.0],
                            [9000, 9.0],
                            [10000, 9.0],
                            [11000, 9.0],
                            [12000, 9.0],
                            [13000, 9.0],
                            [14000, 9.0],
                            [15000, 8.0],
                            [16000, 7.0],
                            [17000, 6.0],
                            [18000, 5.0],
                            [19000, 4.0],
                        ]
                    },
                }
            },
            "series": {
                "input": [
                    [0, 0.0],
                    [1000, 1.0],
                    [2000, 2.0],
                    [3000, 3.0],
                    [4000, 4.0],
                    [5000, 5.0],
                    [6000, 6.0],
                    [7000, 7.0],
                    [8000, 8.0],
                    [9000, 9.0],
                    [10000, 9.0],
                    [11000, 8.0],
                    [12000, 7.0],
                    [13000, 6.0],
                    [14000, 5.0],
                    [15000, 4.0],
                    [16000, 3.0],
                    [17000, 2.0],
                    [18000, 1.0],
                    [19000, 0.0],
                ]
            },
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
        factory.add_source(InputRef('input'))
        node = factory.build()

        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'input':series})

        expected = {
            "anomalies": [],
            "series": {
                "input": [
                    [0, 0.0],
                    [1000, 1.0],
                    [2000, 2.0],
                    [3000, 3.0],
                    [4000, 4.0],
                    [5000, 5.0],
                    [6000, 6.0],
                    [7000, 7.0],
                    [8000, 8.0],
                    [9000, 9.0],
                    [10000, 9.0],
                    [11000, 8.0],
                    [12000, 7.0],
                    [13000, 6.0],
                    [14000, 5.0],
                    [15000, 4.0],
                    [16000, 3.0],
                    [17000, 2.0],
                    [18000, 1.0],
                    [19000, 0.0],
                ]
            },
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

import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.mock import NoBaseline
from model.pipeline.params.float import Float, BoundedFloat
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

from model.utils import timestamp_to_epoch

class TestSimpleThreshold(unittest.TestCase):

    def test_simple_threshold(self):
        series = self.build_triangle()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], series.as_list())
        
        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.set_param_value('inside', True)
        factory.set_param_value('strict', False)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(series, st, [[0, 6],[14, 20]])

        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.set_param_value('inside', True)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(series, st, [[1, 5],[15, 19]])

        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.set_param_value('inside', False)
        factory.set_param_value('strict', False)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(series, st, [[0, 1], [5, 15], [19, 20]])

        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.set_param_value('inside', False)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(series, st, [[6, 14]])

    def case(self, series, node, expected_anomalies):
        pipeline = Pipeline(node)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)
        anomalies = analysis.anomalies

        self.assertEqual(len(expected_anomalies), len(anomalies))
        for i in range(len(expected_anomalies)):
            expected_anomaly = expected_anomalies[i]
            self.assertEqual({
                'algo_id': str(node),
                'desc': None,
                'from': expected_anomaly[0]*1000,
                'to': expected_anomaly[1]*1000,
                'score': 1.0
            },anomalies[i].output_format())

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

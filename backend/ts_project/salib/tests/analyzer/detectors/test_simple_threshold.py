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

class TestSimpleThreshold(unittest.TestCase):

    def test_simple_threshold_case_inside(self):
        factory = self.prepare_factory()
        factory.set_param_value('inside', True)
        factory.set_param_value('strict', False)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[0, 6, 1.0],[14, 20, 1.0]])

    def test_simple_threshold_case_inside_strict(self):
        factory = self.prepare_factory()
        factory.set_param_value('inside', True)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[1, 5, 1.0],[15, 19, 1.0]])

    def test_simple_threshold_case(self):
        factory = self.prepare_factory()
        factory.set_param_value('inside', False)
        factory.set_param_value('strict', False)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[0, 1, 0.0], [5, 15, 1.0], [19, 20, 0.0]])

    def test_simple_threshold_case_strict(self):
        factory = self.prepare_factory()
        factory.set_param_value('inside', False)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', 0)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[6, 14, 1.0]])

    def test_simple_threshold_none_edges_strict(self):
        series = self.build_triangle()
        
        factory = self.prepare_factory()
        factory.set_param_value('inside', False)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', None)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[6, 14, 1.0]])

    def test_simple_threshold_none_edges_inside_strict(self):
        factory = self.prepare_factory()
        factory.set_param_value('inside', True)
        factory.set_param_value('strict', True)
        factory.set_param_value('lower', None)
        factory.set_param_value('upper', 5)
        st = factory.build()

        self.case(st, [[0, 5, 1.0], [15, 20, 1.0]])

    def prepare_factory(self):
        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.add_source(InputRef('input'))
        return factory

    def case(self, node, expected_anomalies):
        series = self.build_triangle()
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'input': series})
        anomalies = analysis.anomalies

        for i in range(len(expected_anomalies)):
            expected_anomaly = expected_anomalies[i]
            self.assertEqual({
                'source_node': node.id,
                'id': anomalies[i].id(),
                'from': expected_anomaly[0]*1000,
                'to': expected_anomaly[1]*1000,
                'score': expected_anomaly[2],
                'source_anomalies': [],
            },anomalies[i].output_format())
        self.assertEqual(len(expected_anomalies), len(anomalies))

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

        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], raw_values)
        return series

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

class TestQuantile(unittest.TestCase):

    def test_quantile_case(self):
        factory = self.prepare_factory()
        factory.set_param_value('upper', 90)
        factory.set_param_value('lower', 10)
        st = factory.build()

        self.case(st, [[0, 1], [10, 11]])

        factory = self.prepare_factory()
        factory.set_param_value('upper', 100)
        factory.set_param_value('lower', 10)
        st = factory.build()

        self.case(st, [[0, 1]])

        factory = self.prepare_factory()
        factory.set_param_value('upper', 90)
        factory.set_param_value('lower', 0)
        st = factory.build()

        self.case(st, [[10, 11]])

        factory = self.prepare_factory()
        factory.set_param_value('upper', 100)
        factory.set_param_value('lower', 50)
        st = factory.build()

        self.case(st, [[0, 5]])

        factory = self.prepare_factory()
        factory.set_param_value('upper', 50)
        factory.set_param_value('lower', 0)
        st = factory.build()

        self.case(st, [[6, 11]])

    def test_quantile_edge_case(self):
        factory = self.prepare_factory()
        factory.set_param_value('upper', 100)
        factory.set_param_value('lower', 0)
        st = factory.build()

        self.case(st, [])

    def prepare_factory(self):
        factory = NodeFactory.detector('test', 'Quantile')
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
                'duration': expected_anomaly[1]-expected_anomaly[0],
                'score': 1.0,
                'source_anomalies': [],
            },anomalies[i].output_format())
        self.assertEqual(len(expected_anomalies), len(anomalies))

    def build_triangle(self):
        sb_up = TestSeriesBuilder.linear(11, 0, 1)
        series = sb_up.build()
        raw_values = series.as_list()
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], raw_values)
        return series

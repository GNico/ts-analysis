import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.params.float import Float, BoundedFloat
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

from model.utils import timestamp_to_epoch_secs

class TestShift(unittest.TestCase):

    def test_shift_positive(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '1s')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, 1, 10)

    def test_shift_negative(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '-1s')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, -1, 8)

    def test_shift_edge_case(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '0')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, 0, 9)

    def case(self, series, node, start, end):
        pipeline = Pipeline(node)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)
        result = analysis.result_for_node(node.id)

        self.assertEqual(start, timestamp_to_epoch_secs(result.series.start))
        self.assertEqual(end, timestamp_to_epoch_secs(result.series.end))

    def build_test_series(self):
        series = TestSeriesBuilder.linear(10, 0, 1).build()
        self.assertEqual(0, timestamp_to_epoch_secs(series.start))
        self.assertEqual(9, timestamp_to_epoch_secs(series.end))
        return series
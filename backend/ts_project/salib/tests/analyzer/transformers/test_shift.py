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
        self.case(series, stdnormalize, 2, 4, [[2000, 0.0], [3000, 1.0], [4000, 2.0]])

    def test_shift_positive_periods(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '1')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, 2, 4, [[2000, 0.0], [3000, 1.0], [4000, 2.0]])

    def test_shift_negative(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '-1s')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, 0, 2, [[0000, 0.0], [1000, 1.0], [2000, 2.0]])

    def test_shift_edge_case(self):
        series = self.build_test_series()
        factory = NodeFactory.transformer('test', 'Shift')
        factory.set_param_value('delta', '0')
        stdnormalize = factory.build()
        self.case(series, stdnormalize, 1, 3, [[1000, 0.0], [2000, 1.0], [3000, 2.0]])

    def case(self, series, node, start, end, json):
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline)
        # TODO: define named inputs
        analysis = analyzer.analyze(series)
        result = analysis.result_for_node(node.id)

        self.assertEqual(start, timestamp_to_epoch_secs(result.series.start))
        self.assertEqual(end, timestamp_to_epoch_secs(result.series.end))
        self.assertEqual(json, result.series.output_format())

    def build_test_series(self):
        series = TestSeriesBuilder.linear(3, 0, 1, start_time=1).build()
        self.assertEqual(1, timestamp_to_epoch_secs(series.start))
        self.assertEqual(3, timestamp_to_epoch_secs(series.end))
        return series
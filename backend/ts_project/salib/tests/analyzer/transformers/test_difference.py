import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestDifference(unittest.TestCase):

    def test_base_substraction(self):
        series1 = TestSeriesBuilder.linear(10, 0, 1).build()
        series2 = TestSeriesBuilder.linear(10, 1, 1).build()

        factory = NodeFactory.transformer('test', 'Difference')
        factory.set_param_value('metric', 'sub')
        diff = factory.build()

        result, debug_info = diff.transform([series1, series2], False)

        expected_series = [-1] * 10
        self.assertEqual(expected_series, list(result.values))


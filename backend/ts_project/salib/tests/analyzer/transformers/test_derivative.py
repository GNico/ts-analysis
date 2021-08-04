import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestDerivative(unittest.TestCase):

    def test_base_derivative(self):
        series1 = TestSeriesBuilder.linear(10, 0, 1).build()

        factory = NodeFactory.transformer('test', 'Derivative')
        factory.set_param_value('lag', '1')
        factory.set_param_value('metric', 'sub')
        diff = factory.build()

        result, debug_info = diff.transform([series1], False)

        expected_series = [1.0] * 9
        self.assertEqual(expected_series, list(result.values))


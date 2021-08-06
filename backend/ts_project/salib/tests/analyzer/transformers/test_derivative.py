import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.series import Series
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestDerivative(unittest.TestCase):

    def test_base_derivative(self):
        self.maxDiff = None
        series1 = TestSeriesBuilder.linear(5, 0, 1).build()

        factory = NodeFactory.transformer('test', 'Derivative')
        factory.set_param_value('lag', '1')
        factory.set_param_value('metric', 'sub')
        diff = factory.build()

        result, debug_info = diff.transform([series1], False)

        expected_series = Series.from_array([
            [1, 1],
            [2, 1],
            [3, 1],
            [4, 1],
            ])

        self.assertEqual(list(expected_series.pdseries.index), list(result.index))
        self.assertEqual(list(expected_series.pdseries.values), list(result.values))

    def test_base_derivative_non_linear(self):
        self.maxDiff = None
        series1 = Series.from_array([
            [0, 1],
            [1, 2],
            [2, 4],
            [3, 0],
            [4, 16],
        ])

        factory = NodeFactory.transformer('test', 'Derivative')
        factory.set_param_value('lag', '1')
        factory.set_param_value('metric', 'sub')
        diff = factory.build()

        result, debug_info = diff.transform([series1], False)

        expected_series = Series.from_array([
            [1, 1],
            [2, 2],
            [3, -4],
            [4, 16],
        ])

        self.assertEqual(list(expected_series.pdseries.index), list(result.index))
        self.assertEqual(list(expected_series.pdseries.values), list(result.values))


    def test_base_derivative_lag2(self):
        series1 = TestSeriesBuilder.linear(5, 0, 1).build()

        factory = NodeFactory.transformer('test', 'Derivative')
        factory.set_param_value('lag', '2')
        factory.set_param_value('metric', 'sub')
        diff = factory.build()

        result, debug_info = diff.transform([series1], False)

        expected_series = Series.from_array([
            [2, 2],
            [3, 2],
            [4, 2],
            ])

        self.assertEqual(list(expected_series.pdseries.index), list(result.index))
        self.assertEqual(list(expected_series.pdseries.values), list(result.values))
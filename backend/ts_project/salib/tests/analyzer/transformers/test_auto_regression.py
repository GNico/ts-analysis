import numpy as np
import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestAutoRegression(unittest.TestCase):

    def test_linear_series_lags(self):
        series = TestSeriesBuilder.linear(10, 0, 1).build()

        factory = NodeFactory.transformer('test', 'AutoRegression')
        factory.set_param_value('p', '1')
        factory.set_param_value('d', 1)
        diff = factory.build()

        result = diff.transform([series])

        expected_series = [0] * 8
        actual_series = list(result.values)
        for i in range(0, len(expected_series)):
            self.assertAlmostEqual(expected_series[i], actual_series[i], 2)

    def test_seesaw(self):
        series = Series.from_array([
            [0, 1],
            [1, -1],
            [2, 1],
            [3, -1],
            [4, 1],
            [5, -1]
            ], 1)

        factory = NodeFactory.transformer('test', 'AutoRegression')
        factory.set_param_value('p', '1')
        diff = factory.build()

        result = diff.transform([series])

        expected_series = [0] * 5
        actual_series = list(result.values)
        for i in range(0, len(expected_series)):
            self.assertAlmostEqual(expected_series[i], actual_series[i], 2)

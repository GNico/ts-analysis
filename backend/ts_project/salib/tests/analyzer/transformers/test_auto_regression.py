import numpy as np
import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestAutoRegression(unittest.TestCase):

    def test_linear_series_lags(self):
        series = TestSeriesBuilder.linear(10, 0, 1).build()

        factory = NodeFactory.transformer('test', 'AutoRegression')
        factory.set_param_value('lags', '2')
        factory.set_param_value('period', '0')
        diff = factory.build()

        result = diff.transform([series])

        expected_series = [0] * 8
        actual_series = list(result.values)
        self.assertEqual(len(expected_series), len(actual_series))
        for i in range(0, len(expected_series)):
            self.assertAlmostEqual(expected_series[i], actual_series[i])

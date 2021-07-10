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

EXPECTED_KEYS = set([
        'ADF: Critical Value (10%)',
        'ADF: Critical Value (1%)',
        'ACF: lag_correlations',
        'PACF: lag_correlations',
        'ADF: Test Statistic',
        'ADF: p-value',
        'ADF: # lags used',
        'ADF: Observations',
        'ADF: Critical Value (5%)'])

class TestIdentity(unittest.TestCase):

    def test_linear_series_lags(self):
        series = TestSeriesBuilder.linear(10, 0, 1).build()

        factory = NodeFactory.transformer('test', 'Identity')
        factory.set_param_value('adf_test', True)
        factory.set_param_value('acf', True)
        factory.set_param_value('pacf', True)
        identity = factory.build()

        result, debug_info = identity.transform([series], True)

        expected_series = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        actual_series = list(result.values)
        for i in range(0, len(expected_series)):
            self.assertEqual(expected_series[i], actual_series[i])
        # With debug info
        self.assertEqual(EXPECTED_KEYS, set(debug_info.keys()))

        # No debug info
        result, debug_info = identity.transform([series], False)
        self.assertEqual([], list(debug_info.keys()))

    def test_seesaw(self):
        series = Series.from_array([
            [0, 1],
            [1, -1],
            [2, 1],
            [3, -1],
            [4, 1],
            [5, -1]
            ], 1)

        factory = NodeFactory.transformer('test', 'Identity')
        factory.set_param_value('adf_test', True)
        factory.set_param_value('acf', True)
        factory.set_param_value('pacf', True)
        identity = factory.build()

        result, debug_info = identity.transform([series], True)

        # With debug info
        self.assertEqual(EXPECTED_KEYS, set(debug_info.keys()))

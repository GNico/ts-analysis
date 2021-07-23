import pandas as pd
import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.testcase import TestCase


class TestDivide(unittest.TestCase):

    def test_divide(self):
        series1 = Series.from_array([
            [1, 1],
            [2, 2],
            [3, 3]]
            , 1)
        series2 = Series.from_array([
            [2, 2],
            [3, 0],
            [4, 5]]
            , 1)
        factory = NodeFactory.transformer('test', 'Divide')
        divide = factory.build()

        result, debug_info = divide.transform([series1, series2], False)
        expected_series = pd.Series([1.0, 0.0], index=series1.pdseries.index[1:3])
        self.assertEqual(list(expected_series.index), list(result.index))
        self.assertEqual(list(expected_series.values), list(result.values))


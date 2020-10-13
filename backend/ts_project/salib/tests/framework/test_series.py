import pandas as pd
import unittest
from model.series import Series


class TestSeries(unittest.TestCase):

    def test_series_from_array(self):

        test_s = Series.from_array([
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 1],
            [6, 0]
        ], 1, 's')

        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), test_s.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:06'), test_s.end)
        self.assertEqual(1, test_s.interval)
        self.assertEqual(7, test_s.span())

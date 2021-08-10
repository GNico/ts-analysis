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
        ])
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), test_s.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:06'), test_s.end)
        self.assertEqual(1, test_s.interval.seconds)
        self.assertEqual(7, test_s.span())

    def test_series_output_format(self):
        test_s = Series.from_array([
            [0, 0],
            [1, 1]
        ])
        self.assertEqual([[0, 0.0], [1000, 1.0]], test_s.output_format())

    def test_series_infer_freq_error(self):
        try:
            Series.from_array([
                [0, 0],
                [1, 1],
                [2, 0],
                [4, 0],
                [5, 1],
                [6, 0]
            ])
        except ValueError as e:
            self.assertEqual("""Index must be equally spaced, could not infer frequency
Index: DatetimeIndex(['1970-01-01 00:00:00', '1970-01-01 00:00:01',
               '1970-01-01 00:00:02', '1970-01-01 00:00:04',
               '1970-01-01 00:00:05', '1970-01-01 00:00:06'],
              dtype='datetime64[ns]', freq=None)
Deltas: [1000000000 2000000000]""", str(e))
        else:
            self.fail('Should throw')
import pandas as pd
import unittest

import model.utils as utils

class TestSeries(unittest.TestCase):

    def test_lags_spec(self):
        self.lags_case('2', '1h', [1, 2])
        self.lags_case('2,3', '1h', [2, 3])
        self.lags_case('2h, 3h', '1h', [2, 3])
        self.lags_case('0-12h', '1h', list(range(1, 13)))
        self.lags_case('0-12h, 24h-48h', '1h', list(range(1, 13))+list(range(24, 49)))

    def test_period_str2int_numbers(self):
        self.case('2', '2h', 2)
        self.case('20', '30m', 20)

    def test_period_str2int(self):
        self.case('2h', '2h', 1)
        self.case('2h', '30m', 4)
        self.case('12h', '2h', 6)
        self.case('1d', '1h', 24)
        self.case('3h', '2h', 1)
        self.case('5h', '2h', 2)

    def test_period_str2int_edge_cases(self):
        self.case('3h', '6h', 0, False)
        self.case('-2h', '2h', -1)

    def test_invalid_period(self):
        self.case_error('2h', '4h', True)
        self.case_error('3h', '200m', True)

    def lags_case(self, str_spec, base_period_str, expected, validate=True):
        base_period = pd.Timedelta(base_period_str)
        self.assertEqual(expected, utils.lags_range_timedelta_to_period(str_spec, base_period, validate))

    def case(self, str_period, base_period_str, expected, validate=True):
        base_period = pd.Timedelta(base_period_str)
        self.assertEqual(expected, utils.timedelta_to_period(str_period, base_period, validate))

    def case_error(self, str_period, base_period_str, validate):
        base_period = pd.Timedelta(base_period_str)
        self.assertRaises(ValueError, utils.timedelta_to_period, str_period, base_period, validate)
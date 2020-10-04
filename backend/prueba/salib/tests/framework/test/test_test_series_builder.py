import pandas as pd
import unittest

from model.test import test_series_builder as tsb


class TestTestCase(unittest.TestCase):

    def test_build_basic(self):
        builder = tsb.TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        series = builder.build()
        self.assertEqual(2, series.span())

    def test_append_two_series(self):
        builder1 = tsb.TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        builder2 = tsb.TestSeriesBuilder([
            [1, 2],
            [2, 2]
            ], 1, 's')
        builder1.append(builder2)
        series = builder1.build()
        self.assertEqual(4, series.span())
        self.assertEqual([1, 1, 2, 2], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

    def test_compose_two_series(self):
        builder1 = tsb.TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        builder2 = tsb.TestSeriesBuilder([
            [0, 2],
            [1, 2]
            ], 1, 's')
        builder1.compose(builder2)
        series = builder1.build()
        self.assertEqual(2, series.span())
        self.assertEqual([3, 3], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:01'), series.end)

    def test_build_constant(self):
        series = tsb.TestSeriesBuilder.constant(10).build()
        self.assertEqual(10, series.span())
        self.assertEqual([0]*10, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

        series = tsb.TestSeriesBuilder.constant(5, 2, 2, 's').build()
        self.assertEqual(5, series.span())
        self.assertEqual([2]*5, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:08'), series.end)

    def test_compose_constants(self):
        builder = tsb.TestSeriesBuilder.constant(10, 1)
        builder.compose(tsb.TestSeriesBuilder.constant(10, 2))
        series = builder.build()
        self.assertEqual(10, series.span())
        self.assertEqual([3]*10, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

    def test_build_linear(self):
        series = tsb.TestSeriesBuilder.linear(10, 0, 1).build()
        self.assertEqual(10, series.span())
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

        series = tsb.TestSeriesBuilder.linear(4, 2, -2).build()
        self.assertEqual(4, series.span())
        self.assertEqual([2, 0, -2 , -4], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

    def test_build_linear_compose(self):
        builder = tsb.TestSeriesBuilder.constant(4, 1)
        builder.compose(tsb.TestSeriesBuilder.linear(4, 0, -2))
        series = builder.build()
        self.assertEqual(4, series.span())
        self.assertEqual([1, -1, -3, -5], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)
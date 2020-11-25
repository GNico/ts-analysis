import pandas as pd
import unittest

from model.test.test_series_builder import TestSeriesBuilder


class TestTestCase(unittest.TestCase):

    def test_build_basic(self):
        builder = TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        series = builder.build()
        self.assertEqual(2, series.span())

    def test_append_two_series(self):
        builder1 = TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        builder2 = TestSeriesBuilder([
            [1, 2],
            [2, 2]
            ], 1, 's')
        builder1.append(builder2)
        series = builder1.build()
        self.assertEqual(4, series.span())
        self.assertEqual([1, 1, 2, 2], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

    def test_append_two_series_piecewise(self):
        builder1 = TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        builder2 = TestSeriesBuilder([
            [1, 2],
            [2, 2]
            ], 1, 's')
        builder1.append(builder2, True)
        series = builder1.build()
        self.assertEqual(4, series.span())
        self.assertEqual([1, 1, 1, 1], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

    def test_compose_two_series(self):
        builder1 = TestSeriesBuilder([
            [0, 1],
            [1, 1]
            ], 1, 's')
        builder2 = TestSeriesBuilder([
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
        series = TestSeriesBuilder.constant(10).build()
        self.assertEqual(10, series.span())
        self.assertEqual([0]*10, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

        series = TestSeriesBuilder.constant(5, 2, 2, 's').build()
        self.assertEqual(5, series.span())
        self.assertEqual([2]*5, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:08'), series.end)

    def test_compose_constants(self):
        builder = TestSeriesBuilder.constant(10, 1)
        builder.compose(TestSeriesBuilder.constant(10, 2))
        series = builder.build()
        self.assertEqual(10, series.span())
        self.assertEqual([3]*10, series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

    def test_build_linear(self):
        series = TestSeriesBuilder.linear(10, 0, 1).build()
        self.assertEqual(10, series.span())
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:09'), series.end)

        series = TestSeriesBuilder.linear(4, 2, -2).build()
        self.assertEqual(4, series.span())
        self.assertEqual([2, 0, -2, -4], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

    def test_build_linear_compose(self):
        builder = TestSeriesBuilder.constant(4, 1)
        builder.compose(TestSeriesBuilder.linear(4, 0, -2))
        series = builder.build()
        self.assertEqual(4, series.span())
        self.assertEqual([1, -1, -3, -5], series.as_list())
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:00'), series.start)
        self.assertEqual(pd.Timestamp('1970-01-01 00:00:03'), series.end)

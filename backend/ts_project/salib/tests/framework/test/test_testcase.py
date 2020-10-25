import unittest

from model.test.testcase import TestCase
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from tests.framework.mock_analyzer import MockAnalyzer
from model.test import metric_classifications_builder as cb


class TestTestCase(unittest.TestCase):

    def test_metrics_case1(self):
        actual_anomalies = [
            Anomaly.from_epoch(1, 1, 1.0),
            Anomaly.from_epoch(2, 2, 1.0),
            Anomaly.from_epoch(4, 4, 1.0)
        ]

        analyzer = MockAnalyzer(actual_anomalies)

        test_series = Series.from_array([
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 1],
            [6, 0]
        ], 1, 's')

        expected_anomalies = TestCase.anomalies_from_mock_series(test_series)

        expected_analysis = Analysis(
            expected_anomalies,
            None
        )

        test = TestCase("testcase1", test_series, analyzer, expected_analysis)
        result = test.run()
        anomaly_metrics = result.anomaly_metrics

        expected_tp = cb.epochs_to_timestamp([1])
        expected_fp = cb.epochs_to_timestamp([2, 4])
        expected_tn = cb.epochs_to_timestamp([0, 3, 6])
        expected_fn = cb.epochs_to_timestamp([5])

        self.assertEqual(expected_tp, anomaly_metrics.tp)
        self.assertEqual(expected_fp, anomaly_metrics.fp)
        self.assertEqual(expected_tn, anomaly_metrics.tn)
        self.assertEqual(expected_fn, anomaly_metrics.fn)

        self.assertEqual(1, anomaly_metrics.tp_count())
        self.assertEqual(3, anomaly_metrics.tn_count())
        self.assertEqual(2, anomaly_metrics.fp_count())
        self.assertEqual(1, anomaly_metrics.fn_count())

        self.assertAlmostEqual(0.33, anomaly_metrics.precision(), 2)
        self.assertAlmostEqual(0.5, anomaly_metrics.recall(), 2)
        self.assertAlmostEqual(0.4, anomaly_metrics.f1(), 2)

    def test_anomalies_from_mock(self):
        test_series = Series.from_array([
            [0, 0],
            [1, 0],
            [2, 1],
            [3, 0],
            [4, 1],
            [5, 1],
            [6, 0]
        ], 1, 's')

        anomalies = TestCase.anomalies_from_mock_series(test_series)

        self.assertEqual(2, len(anomalies))
        self.assertEqual(test_series.pdseries.index[2], anomalies[0].start)
        self.assertEqual(test_series.pdseries.index[2], anomalies[0].end)
        self.assertEqual(test_series.pdseries.index[4], anomalies[1].start)
        self.assertEqual(test_series.pdseries.index[5], anomalies[1].end)

    def test_anomalies_from_mock_edge_case(self):
        test_series = Series.from_array([
            [0, 1],
            [1, 0],
            [2, 1]
        ], 1, 's')

        anomalies = TestCase.anomalies_from_mock_series(test_series)

        self.assertEqual(2, len(anomalies))
        self.assertEqual(test_series.pdseries.index[0], anomalies[0].start)
        self.assertEqual(test_series.pdseries.index[0], anomalies[0].end)
        self.assertEqual(test_series.pdseries.index[2], anomalies[1].start)
        self.assertEqual(test_series.pdseries.index[2], anomalies[1].end)

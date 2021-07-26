import unittest

from model.test.testcase import TestCase
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from model.pipeline.nodes.node_result import NodeResult
from tests.framework.mock_analyzer import MockAnalyzer
from model.test import metric_classifications_builder as mcb


class TestTestCase(unittest.TestCase):

    def test_metrics_case1(self):
        test_series = Series.from_array([
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 1],
            [6, 1],
            [7, 0]
        ], 1, 's')

        actual_anomalies = [
            Anomaly.from_epoch(1, 1, 1.0),
            Anomaly.from_epoch(2, 2, 1.0),
            Anomaly.from_epoch(4, 4, 1.0)
        ]

        analyzer = MockAnalyzer(actual_anomalies)

        expected_anomalies = TestCase.anomalies_from_mock_series(test_series)

        expected_analysis = Analysis(
            test_series,
            None,
            expected_anomalies,
            False
        )

        test = TestCase("testcase1", test_series, analyzer, expected_analysis)
        result = test.run()
        anomaly_metrics = result.anomaly_metrics

        expected_tp = mcb.epochs_to_timestamp([1])
        expected_fp = mcb.epochs_to_timestamp([2, 4])
        expected_tn = mcb.epochs_to_timestamp([0, 3, 7])
        expected_fn = mcb.epochs_to_timestamp([5, 6])

        self.assertEqual(expected_tp, anomaly_metrics.tp)
        self.assertEqual(expected_fp, anomaly_metrics.fp)
        self.assertEqual(expected_tn, anomaly_metrics.tn)
        self.assertEqual(expected_fn, anomaly_metrics.fn)

        self.assertEqual(1, anomaly_metrics.tp_count())
        self.assertEqual(2, anomaly_metrics.fp_count())
        self.assertEqual(2, anomaly_metrics.fn_count())
        self.assertEqual(3, anomaly_metrics.tn_count())

        expected_tp_ranges = mcb.epochs_to_ranges([[1, 2]])
        expected_fp_ranges = mcb.epochs_to_ranges([[2, 3], [4, 5]])
        expected_fn_ranges = mcb.epochs_to_ranges([[5, 7]])

        self.assertEqual(expected_tp_ranges, anomaly_metrics.tp_ranges)
        self.assertEqual(expected_fp_ranges, anomaly_metrics.fp_ranges)
        self.assertEqual(expected_fn_ranges, anomaly_metrics.fn_ranges)

        self.assertAlmostEqual(0.33, anomaly_metrics.precision(), 2)
        self.assertAlmostEqual(0.33, anomaly_metrics.recall(), 2)
        self.assertAlmostEqual(0.33, anomaly_metrics.f1(), 2)

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

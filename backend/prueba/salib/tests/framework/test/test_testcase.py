import unittest

from model.test import testcase
from model import anomaly
from model import analysis
from model import series
from tests.framework import mock_analyzer
from model.test import metric_classifications_builder as cb


class TestTestCase(unittest.TestCase):

    def test_metrics(self):
        expected_anomalies = [
            anomaly.Anomaly.from_epoch(2, 2, 1.0),
            anomaly.Anomaly.from_epoch(4, 5, 1.0)
        ]

        actual_anomalies = [
            anomaly.Anomaly.from_epoch(1, 2, 1.0),
            anomaly.Anomaly.from_epoch(5, 6, 1.0)
        ]

        test_series = series.Series.from_array([
            [1, 0],
            [2, 1],
            [3, 0],
            [4, 1],
            [5, 1],
            [6, 0]
        ], 1, 's')

        analyzer = mock_analyzer.MockAnalyzer(expected_anomalies)

        expected_analysis = analysis.Analysis(
            "Test",
            actual_anomalies,
            None,
            None
        )

        test = testcase.TestCase(test_series, analyzer, expected_analysis)
        result = test.run()
        anomaly_metrics = result.anomaly_metrics

        expected_tp = cb.interval_from_epoch([[2, 2], [5, 5]])
        expected_fp = cb.interval_from_epoch([[4, 4]])
        expected_tn = cb.interval_from_epoch([[3, 3]])
        expected_fn = cb.interval_from_epoch([[6, 6]])

        self.assertEqual(expected_tp, anomaly_metrics.tp)
        self.assertEqual(expected_fp, anomaly_metrics.fp)
        self.assertEqual(expected_tn, anomaly_metrics.tn)
        self.assertEqual(expected_fn, anomaly_metrics.fn)

        self.assertEqual(0, anomaly_metrics.tp_count())
        self.assertEqual(0, anomaly_metrics.tn_count())
        self.assertEqual(0, anomaly_metrics.fp_count())
        self.assertEqual(0, anomaly_metrics.fn_count())

        self.assertEqual(1, anomaly_metrics.precision())
        self.assertEqual(1, anomaly_metrics.recall())
        self.assertEqual(1, anomaly_metrics.f1())

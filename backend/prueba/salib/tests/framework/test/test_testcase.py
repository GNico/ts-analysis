import unittest

from model.test import testcase
from model import anomaly
from model import analysis
from tests.framework import mock_analyzer


class TestTestCase(unittest.TestCase):

    def test_metrics(self):
        anomalies = [anomaly.Anomaly(1, 2, 1.0),
                     anomaly.Anomaly(3, 4, 1.0)]
        analyzer = mock_analyzer.MockAnalyzer(anomalies)
        # Mock
        series = None
        expected_analysis = analysis.Analysis("Test", anomalies, None, None)
        test = testcase.TestCase(series, analyzer, expected_analysis)
        result = test.run()
        anomaly_metrics = result.anomaly_metrics

        self.assertEqual(0, anomaly_metrics.tp_count())
        self.assertEqual(0, anomaly_metrics.tn_count())
        self.assertEqual(0, anomaly_metrics.fp_count())
        self.assertEqual(0, anomaly_metrics.fn_count())
        # self.assertEqual(1, anomaly_metrics.precision())
        # self.assertEqual(1, anomaly_metrics.recall())
        # self.assertEqual(1, anomaly_metrics.f1())

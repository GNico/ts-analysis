import unittest

import model.test.metric_classifications_builder as cb
from model.anomaly import Anomaly


class TestMetricClassificationsBuilder(unittest.TestCase):

    def test_no_overlap(self):
        anomalies = [
            Anomaly.from_epoch(1, 2),
            Anomaly.from_epoch(2, 6)
        ]
        anomalies = sorted(anomalies)
        cb.assert_no_overlap(anomalies)

    def test_overlap(self):
        anomalies = [
            Anomaly.from_epoch(1, 4),
            Anomaly.from_epoch(3, 6)
        ]
        anomalies = sorted(anomalies)
        self.assertRaises(Exception, cb.assert_no_overlap, anomalies)

    def test_deep_overlap(self):
        anomalies = [
            Anomaly.from_epoch(1, 2),
            Anomaly.from_epoch(3, 4),
            Anomaly.from_epoch(1, 5)
        ]
        anomalies = sorted(anomalies)
        self.assertRaises(Exception, cb.assert_no_overlap, anomalies)

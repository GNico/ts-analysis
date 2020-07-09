from . import metrics
from . import classifications_builder


class Result:

    def __init__(self, test_case, actual_analysis):
        self.test_case = test_case
        self.actual_analysis = actual_analysis
        self.calculate_metrics()

    def calculate_metrics(self):
        self.anomaly_metrics = self.build_anomaly_metrics()

    def build_anomaly_metrics(self):
        expected = self.test_case.expected_analysis.anomalies
        actual = self.actual_analysis.anomalies
        tp, fp, tn, fn = classifications_builder.ClassificationsBuilder.build(
            self.test_case.series,
            expected,
            actual)
        return metrics.Metrics(tp, fp, tn, fn)

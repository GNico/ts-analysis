import json
import os

from .metrics import Metrics
from . import metric_classifications_builder


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
        tp, fp, tn, fn = metric_classifications_builder.build(
            self.test_case.series,
            expected,
            actual)
        return Metrics(tp, fp, tn, fn)

    def id(self):
        return self.test_case.id

    def export_testcase(self):
        output = self.actual_analysis.output_format()
        output['series'] = self.test_case.series.output_format()
        output['metrics'] = self.anomaly_metrics.output_format()
        return output

    def export_all(self):
        output = {}
        output['general'] = 'foo'
        output['testcases'] = [self.export_testcase()]
        return json.dumps(output)

    def export_for_visuals(self):
        output = self.export_all()
        out_path = os.getcwd() + "/../algo_test_output/"
        with open(out_path + self.id() + '.json', 'w') as f:
            print(output, file=f)

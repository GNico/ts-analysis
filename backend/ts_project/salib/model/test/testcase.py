from .result import Result
from model.anomaly import Anomaly


class TestCase:

    def __init__(self, id, series, analyzer, expected_analysis):
        self.id = id
        self.series = series
        self.analyzer = analyzer
        self.expected_analysis = expected_analysis

    def run(self):
        actual_analysis = self.analyzer.analyze(self.series)
        return Result(self, actual_analysis)

    @staticmethod
    def anomalies_from_mock_series(series):
        anomalies = []

        if series.span() > 0:
            if series.pdseries[0] == 1:
                start = series.start
            else:
                start = None

            last = series.start
            for t, val in series.pdseries.items():
                if val == 1 and start is None:
                    start = t
                if val == 0 and start is not None:
                    anomalies.append(Anomaly(series, start, last, 1.0))
                    start = None
                last = t

            if start is not None:
                anomalies.append(Anomaly(series, start, series.end, 1.0))

        return anomalies

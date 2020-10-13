from . import analysis
from . import anomaly


class Analyzer:

    def __init__(self):
        # TODO add configuration
        self.config = {}

    def analyze(self, series):
        # TODO analyzers
        anomaly1 = anomaly.Anomaly(1535529600000, 1540936800000, 0.5)
        anomalies = [anomaly1]
        return analysis.Analysis(anomalies)

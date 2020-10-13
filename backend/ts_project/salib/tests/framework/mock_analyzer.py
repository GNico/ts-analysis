from model import analysis


class MockAnalyzer:

    def __init__(self, anomalies):
        self.anomalies = anomalies

    def analyze(self, pdseries):
        return analysis.Analysis("MockAnalyzer", self.anomalies, None, None)

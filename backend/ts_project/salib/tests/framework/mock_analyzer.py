from model.analysis import Analysis


class MockAnalyzer:

    def __init__(self, anomalies):
        self.anomalies = anomalies

    def analyze(self, pdseries):
        return Analysis(pdseries, None, self.anomalies, None)

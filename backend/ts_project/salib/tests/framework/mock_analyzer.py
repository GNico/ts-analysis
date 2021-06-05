from model.analysis import Analysis


class MockAnalyzer:

    def __init__(self, anomalies):
        self.anomalies = anomalies

    def analyze(self, inputs):
        return Analysis(inputs, None, self.anomalies, False)

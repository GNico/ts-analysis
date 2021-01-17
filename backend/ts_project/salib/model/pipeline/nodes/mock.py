class MockOutputFormat:

    def __init__(self, output):
        self.output = output

    def output_format(self):
        return self.output


class NoAnomalies:

    def anomalies(self, series):
        return []

    def id(self):
        return "NoAnomalies"


class NoBaseline:

    def baseline(self, series):
        return MockOutputFormat([])

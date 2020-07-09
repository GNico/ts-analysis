from . import result


class TestCase:

    def __init__(self, series, analyzer, expected_analysis):
        self.series = series
        self.analyzer = analyzer
        self.expected_analysis = expected_analysis

    def run(self):
        actual_analysis = self.analyzer.analyze(self.series)
        return result.Result(self, actual_analysis)

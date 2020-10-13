from .result import Result


class TestCase:

    def __init__(self, series, analyzer, expected_analysis):
        self.series = series
        self.analyzer = analyzer
        self.expected_analysis = expected_analysis

    def run(self):
        actual_analysis = self.analyzer.analyze(self.series)
        return Result(self, actual_analysis)

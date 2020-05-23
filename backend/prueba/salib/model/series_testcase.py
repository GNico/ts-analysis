from . import series_testcase_result

class SeriesTestCase:

  def __init__(self, pdseries, expected_analysis):
    self.series = pdseries
    self.expected_analysis

  def test(self, analyzer):
    actual = analyzer.analyze(self.series)
    return series_testcase_result.SeriesTestCaseResult(self.expected_analysis, actual)
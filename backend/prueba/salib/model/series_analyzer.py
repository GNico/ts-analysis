from . import series_analysis

class SeriesAnalyzer:

  def __init__(self):
    # TODO add configuration
    self.config = {}

  def analyze(self, pdseries):
    return series_analysis.SeriesAnalysis()
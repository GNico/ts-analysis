from . import series_analysis
from . import series_anomaly

class SeriesAnalyzer:

  def __init__(self):
    # TODO add configuration
    self.config = {}

  def analyze(self, pdseries):
    anomaly1 = series_anomaly.SeriesAnomaly(1535529600000, 1540936800000, 0.5)
    anomalies = [anomaly1]
    return series_analysis.SeriesAnalysis(anomalies)
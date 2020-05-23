class SeriesAnalysis:

  def __init__(self, anomalies):
    self.anomalies = anomalies

  def output_format(self):
    return {   
      "name": "test",
      "anomalies": list(map(lambda a: a.output_format(), self.anomalies)),
      "trend": [],
      "baseline": []
    }
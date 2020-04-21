class SeriesAnalysis:

  def __init__(self):
    self.result = {}

  def output_format(self):
    return {   
      "name": "test",
      "anomalies": [
        {
          "from": 1535529600000,
          "to": 1540936800000,
          "score": 0.5
        }
      ],
      "trend": [],
      "baseline": []
    }
class Analysis:

    def __init__(self, name, anomalies, trend, baseline):
        self.name = name
        self.anomalies = anomalies
        self.trend = trend
        self.baseline = baseline

    def output_format(self):
        anomalies = list(map(lambda a: a.output_format(), self.anomalies))
        baseline = list(map(lambda a: a.output_format(), self.baseline))
        trend = list(map(lambda a: a.output_format(), self.trend))
        return {
            "name": self.name,
            "anomalies": anomalies,
            "trend": trend,
            "baseline": baseline
        }

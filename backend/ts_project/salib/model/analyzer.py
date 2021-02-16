from .analysis import Analysis

class Analyzer:

    def __init__(self, pipeline, config={}):
        self.anomaly_pipeline = pipeline
        self.config = config

    def analyze(self, series):
        result = self.anomaly_pipeline.execute(series)
        anomalies = result.anomalies
        return Analysis(series, result, anomalies)

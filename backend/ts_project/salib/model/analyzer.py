from .analysis import Analysis
from .pipeline.components.mock import NoBaseline

class Analyzer:

    def __init__(self, pipeline,
                 baseline_algo=NoBaseline(),
                 config={}):
        self.anomaly_pipeline = pipeline
        self.baseline_algo = baseline_algo
        self.config = config

    def analyze(self, series):
        anomalies = self.anomaly_pipeline.execute(series)
        baseline = self.baseline_algo.baseline(series)
        return Analysis(series, anomalies, baseline)

from .analysis import Analysis
from .pipeline.nodes.mock import NoBaseline

class Analyzer:

    def __init__(self, pipeline,
                 baseline_algo=NoBaseline(),
                 config={}):
        self.anomaly_pipeline = pipeline
        self.baseline_algo = baseline_algo
        self.config = config

    def analyze(self, series):
        result = self.anomaly_pipeline.execute(series)
        anomalies = result.anomalies
        baseline = self.baseline_algo.baseline(series)
        return Analysis(series, anomalies, baseline)

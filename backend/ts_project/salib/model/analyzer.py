from .analysis import Analysis

class Analyzer:

    def __init__(self, pipeline, config={}):
        self.pipeline = pipeline
        self.config = config

    def analyze(self, inputs):
        result = self.pipeline.execute(inputs)
        anomalies = result.anomalies
        return Analysis(inputs, result, anomalies)

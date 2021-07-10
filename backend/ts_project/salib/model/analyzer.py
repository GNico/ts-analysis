from .analysis import Analysis

class Analyzer:

    def __init__(self, pipeline, debug):
        self.pipeline = pipeline
        self.debug = debug

    def analyze(self, inputs):
        result = self.pipeline.execute(inputs, self.debug)
        anomalies = result.anomalies
        return Analysis(inputs, result, anomalies, self.debug)

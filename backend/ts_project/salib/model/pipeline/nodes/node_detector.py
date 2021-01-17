from .node import Node
from .node_result import NodeResult

class NodeDetector(Node):

    def __init__(self):
        super().__init__()

    def execute(self, inputs):
        if len(inputs) != 1:
            raise Exception("Invalid pipeline setup, NodeDetector must have exactly 1 input")
        series = inputs[0].series
        anomalies = self.anomalies(series)
        for anomaly in anomalies:
            anomaly.tag_algo(self.id())
        return NodeResult(self, series=series, anomalies=anomalies)

    def anomalies(self, series):
        raise Exception('Unimplemented method')
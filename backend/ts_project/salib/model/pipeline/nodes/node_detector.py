from .node import Node
from .node_result import NodeResult

class NodeDetector(Node):

    def __init__(self, id):
        super().__init__(id)

    def execute(self, inputs):
        if len(inputs) != 1:
            raise Exception("NodeDetector must have exactly 1 input")
        input = inputs[0]
        anomalies = self.anomalies(input)
        for anomaly in anomalies:
            anomaly.tag_algo(str(self))
        return NodeResult(self, series=input, anomalies=anomalies)

    def anomalies(self, series):
        raise Exception('Unimplemented anomalies method for NodeDetector')
from .node import Node
from .node_result import NodeResult
from ...anomaly import Anomaly

class NodeDetector(Node):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['input'])

    def execute(self, inputs):
        input = inputs[0]
        anomalies = self.anomalies(input)
        for anomaly in anomalies:
            anomaly.set_source_node(self)
        return NodeResult(self, inputs=inputs, output_series=input.output_series, anomalies=anomalies)

    def anomalies(self, series):
        raise Exception('Unimplemented anomalies method for NodeDetector')

    @staticmethod
    def pointwise_consecutive(predicate, series):
        anomalies = []
        current_start = None
        for elem in series.pdseries.items():
            if predicate(elem[1]):
                if current_start is None:
                    current_start = elem[0]
            else:
                if current_start is not None:
                    anomaly = Anomaly(series, current_start, elem[0], 1.0)
                    anomalies.append(anomaly)
                    current_start = None

        if current_start is not None:
            anomaly = Anomaly(series, current_start, series.end_bound(), 1.0)
            anomalies.append(anomaly)

        return anomalies
from .node import Node
from .node_result import NodeResult
from ...anomaly import Anomaly

class NodeDetector(Node):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['input'])

    def execute(self, inputs, debug):
        input = inputs[0]
        anomalies, debug_info = self.anomalies(input.find_output_series(), debug)
        NodeDetector.normalize_anomalies(anomalies, self)
        return NodeResult(self, inputs=inputs, anomalies=anomalies, debug_info=debug_info)

    def anomalies(self, series, debug):
        raise Exception('Unimplemented anomalies method for NodeDetector')

    @staticmethod
    def normalize_anomalies(anomalies, node=None):
        # Normalize and set source node
        max_score = max([anomaly.score for anomaly in anomalies]) if len(anomalies) > 0 else None
        for anomaly in anomalies:
            if node is not None:
                anomaly.set_source_node(node)
            if max_score > 0:
                anomaly.score = anomaly.score / max_score

    @staticmethod
    def pointwise_consecutive(anomaly_scoring, series):
        anomalies = []
        current_start = None
        current_score_sum = None
        current_consecutive_count = None
        for elem in series.pdseries.items():
            anomaly_score = anomaly_scoring(elem[1])
            if anomaly_score is not None:
                if current_start is None:
                    current_start = elem[0]
                    current_score_sum = anomaly_score
                    current_consecutive_count = 1
                else:
                    current_score_sum += anomaly_score
                    current_consecutive_count += 1
            else:
                if current_start is not None:
                    avg_score = current_score_sum / current_consecutive_count
                    anomaly = Anomaly(current_start, elem[0], avg_score)
                    anomalies.append(anomaly)
                    current_start = None


        if current_start is not None:
            avg_score = current_score_sum / current_consecutive_count
            anomaly = Anomaly(current_start, series.end_bound(), avg_score)
            anomalies.append(anomaly)

        return anomalies
from ..node import Node
from ..node_result import NodeResult

class Or(Node):

    def __init__(self):
        super().__init__()

    def execute(self, inputs):
        or_anomalies = []
        for i in inputs:
            or_anomalies.extend(i.anomalies)
        return NodeResult(self, anomalies=or_anomalies)

    def id(self):
        return "OR"

    def desc(self):
        return "Combine all anomalies from sources"
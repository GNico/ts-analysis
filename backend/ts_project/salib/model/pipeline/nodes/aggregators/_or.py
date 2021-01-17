from ..node import Node
from ..node_result import NodeResult

class Or(Node):

    def __init__(self, id):
        super().__init__(id)

    def execute(self, inputs):
        or_anomalies = []
        for i in inputs:
            or_anomalies.extend(i.anomalies)
        return NodeResult(self, anomalies=or_anomalies)

    def __str__(self):
        return 'OR(' + ','.join([s.id for s in self.sources]) + ')'

    def desc(self):
        return 'Combine all anomalies from sources'
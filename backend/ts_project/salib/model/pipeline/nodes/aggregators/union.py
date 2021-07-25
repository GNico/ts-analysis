from ..node import Node
from ..node_result import NodeResult

class Union(Node):

    def __init__(self, id):
        super().__init__(id)

    def execute(self, inputs, debug):
        or_anomalies = []
        for i in inputs:
            or_anomalies.extend(i.anomalies)
        return NodeResult(self, inputs=inputs, anomalies=or_anomalies)

    def __str__(self):
        return 'Union(' + ','.join(map(str, self.sources)) + ')[' + self.id + ']'

    def desc(self):
        return 'Combine all anomalies from sources'

    def display(self):
        return 'Union'

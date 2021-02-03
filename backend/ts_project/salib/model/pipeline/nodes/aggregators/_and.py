from ..node import Node
from ..node_result import NodeResult

class And(Node):

    def __init__(self, id):
        super().__init__(id)

    def execute(self, inputs):
        all_anomalies = []
        # ToDo implement combining overalpping. 
        # On overlap combine
        for i in inputs:
            all_anomalies.extend(i.anomalies)
        return NodeResult(self, anomalies=or_anomalies)

    def __str__(self):
        return 'AND(' + ','.join([s.id for s in self.sources]) + ')'

    def desc(self):
        return 'Combine overlapping anomalies from sources'

    def display(self):
        return 'And'

from ..node import Node
from ..node_result import NodeResult

class And(Node):

    def __init__(self):
        super().__init__()

    def execute(self, inputs):
        all_anomalies = []
        # ToDo implement overalpping. 
        # On overlap do what?
        for i in inputs:
            all_anomalies.extend(i.anomalies)
        return NodeResult(self, anomalies=or_anomalies)

    def id(self):
        return "AND"

    def desc(self):
        return "Combine overlapping anomalies from sources"
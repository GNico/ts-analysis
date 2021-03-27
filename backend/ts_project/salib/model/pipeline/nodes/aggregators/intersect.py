from ..node import Node
from ..node_result import NodeResult
from ...params.boolean import Boolean
from ....anomaly import Anomaly

class Intersect(Node):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('strict', 'Strict', 'If true anomalies must match exact bounds, otherwise, any overlap is considered valid', True))

    def execute(self, inputs):
        if len(inputs) == 1:
            all_anomalies = inputs.anomalies
        else:
            all_anomalies = inputs[0].anomalies
            for i in inputs[1:]:
                all_anomalies = self.join(all_anomalies, i.anomalies)
        return NodeResult(self, inputs=inputs, anomalies=all_anomalies)

    def join(self, lhss, rhss):
        # TODO: should return new anomalies as intersections (as parameter probably, "merge") 
        strict = self.get_param('strict').value
        result = []
        for lhs in lhss:
            for rhs in rhss:                
                if strict:
                    if lhs.start == rhs.start and lhs.end == rhs.end:
                        result.append(lhs)
                        result.append(rhs)
                else:
                    if (lhs.start >= rhs.start and lhs.start <= rhs.end) or (lhs.end >= rhs.start and lhs.end <= rhs.end):
                        result.append(lhs)
                        result.append(rhs)
        return list(set(result)) # Remove duplicates

    def __str__(self):
        return 'Intersect(' + ','.join([s.id for s in self.sources]) + ')'

    def desc(self):
        return 'Combine and merge overlapping anomalies from sources'

    def display(self):
        return 'Intersect'
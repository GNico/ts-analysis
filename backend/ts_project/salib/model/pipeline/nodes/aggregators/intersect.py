from ..node import Node
from ..node_result import NodeResult
from ...params.boolean import Boolean
from ...params.select import Select, SelectOption
from ...params.condition.param_equals_value import ParamEqualsValue
from ....anomaly import Anomaly

class Intersect(Node):

    def __init__(self, id):
        super().__init__(id)
        resolution_options = [
            SelectOption('temporal', 'Temporal'),
            SelectOption('anomaly', 'Anomaly')
        ]
        self.add_required_param(Select('resolution', 'Resolution', 'Combine using temporal axis or anomaly wise', resolution_options, resolution_options[0].code))
        strictness = Boolean('strict', 'Strict', 'If true anomalies must match exact bounds, otherwise, any overlap is considered valid', True)
        strictness.add_condition(ParamEqualsValue('resolution', 'anomaly'))
        self.add_param(strictness)

    def execute(self, inputs, debug):
        if len(inputs) == 1:
            all_anomalies = inputs.anomalies
        else:
            all_anomalies = inputs[0].anomalies
            for i in inputs[1:]:
                all_anomalies = self.join(all_anomalies, i.anomalies)
        return NodeResult(self, inputs=inputs, anomalies=all_anomalies)

    def join(self, lhss, rhss):
        resolution = self.get_param('resolution').value
        if resolution == 'anomaly':
            return self.anomaly_wise_join(lhss, rhss)
        elif resolution == 'temporal':
            return self.temporal_join(lhss, rhss)
        else:
            raise ValueError("Invalid resolution, must be one of " + str(self.get_param('resolution').options))

    def anomaly_wise_join(self, lhss, rhss):
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

    def temporal_join(self, lhss, rhss):
        # TODO consider issue with taking lhs series
        result = []
        for lhs in lhss:
            for rhs in rhss:
                if lhs.start == rhs.start and lhs.end == rhs.end:
                    score = Intersect.combined_scores(lhs, rhs)
                    desc = Intersect.combined_desc(lhs, rhs)
                    new_anomaly = Anomaly(lhs.series, lhs.start, lhs.end, score, desc)
                    result.append(new_anomaly)
                else:
                    fst, snd = sorted((lhs,rhs))
                    # Total inclusion
                    if snd.start >= fst.start and snd.end <= fst.end:
                        score = Intersect.combined_scores(lhs, rhs)
                        desc = Intersect.combined_desc(lhs, rhs)
                        new_anomaly = Anomaly(lhs.series, snd.start, snd.end, score, desc)
                        result.append(new_anomaly)
                    # Partial inclusion
                    elif fst.end >= snd.start and fst.end <= snd.end:
                        score = Intersect.combined_scores(lhs, rhs)
                        desc = Intersect.combined_desc(lhs, rhs)
                        new_start = snd.start
                        new_end = fst.end
                        if new_start < new_end:
                            new_anomaly = Anomaly(lhs.series, new_start, fst.end, score, desc)
                            result.append(new_anomaly)


        return list(set(result)) # Remove duplicates

    @staticmethod
    def combined_scores(lhs, rhs):
        return max(lhs.score, rhs.score)

    @staticmethod
    def combined_desc(lhs, rhs):
        return 'Intersecting(' + str(lhs.desc) + ',' + str(rhs.desc) + ')'

    def __str__(self):
        return 'Intersect(' + ','.join([s.id for s in self.sources]) + ')[' + self.get_param('resolution').value + ']'

    def desc(self):
        return 'Combine and merge overlapping anomalies from sources'

    def display(self):
        return 'Intersect'
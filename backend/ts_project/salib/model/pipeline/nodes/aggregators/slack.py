import numpy as np

from ..node import Node
from ..node_result import NodeResult
from ...params.int import BoundedInt
from ...params.string import String
from ....anomaly import Anomaly
from ....utils import timedelta_to_period

class Slack(Node):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(BoundedInt('slack', 'Slack (%)', 'Anomaly extension as % of anomaly span', 0, None, 25))
        self.add_required_param(String('min_span', 'Min. span', "Min. anomaly span to extend (intervals or period, ej '3h'. Leave empty to ignore.", ''))

    def execute(self, inputs, debug):
        all_anomalies = []
        for i in inputs:
            all_anomalies += i.anomalies

        slack, min_span = self.get_params()
        step = Slack.validated_step(inputs)
        if min_span == '' or min_span is None:
            calc_min_span = None
        else:
            calc_min_span = step * timedelta_to_period(min_span, step)

        new_anomalies, debug_info = self.join(all_anomalies, slack, calc_min_span, debug)

        return NodeResult(self, inputs=inputs, anomalies=new_anomalies, debug_info=debug_info)

    def join(self, all_anomalies, slack, min_span, debug):
        new_anomalies = []
        debug_info = {}

        side_slack = 0.01*(slack / 2)
        for anomaly in all_anomalies:
            # Apply slack
            to_extend = anomaly.span() * side_slack
            new_anomaly = anomaly.copy()
            new_anomaly.start = anomaly.start - to_extend
            new_anomaly.end = anomaly.end + to_extend
            # Extend for min_span
            current_span = new_anomaly.span()
            if min_span is not None and current_span < min_span:
                to_extend = (min_span - current_span)/2
                new_anomaly.start -= to_extend
                new_anomaly.end += to_extend
            # Check if we have made any modifications (edge params case)
            if new_anomaly != anomaly:
                new_anomaly.set_source_anomalies([anomaly])
                new_anomaly.set_source_node(self)
            new_anomalies.append(new_anomaly)

        # Combine
        self.combine(new_anomalies)

        # Remove intermediate anomaly references

        return new_anomalies, debug_info

    def combine(self, anomalies):
        pass

    def combine_pair(self, lhs, rhs):
        result = []
        if lhs.start == rhs.start and lhs.end == rhs.end:
            score = Slack.combined_scores(lhs, rhs)
            new_anomaly = Anomaly(lhs.start, lhs.end, score)
            new_anomaly.set_source_anomalies([lhs, rhs])
            new_anomaly.set_source_node(self)
            result = [new_anomaly]
        else:
            fst, snd = sorted((lhs,rhs))
            # Total inclusion
            if snd.start >= fst.start and snd.end <= fst.end:
                score = Slack.combined_scores(lhs, rhs)
                new_anomaly = Anomaly(fst.start, fst.end, score)
                new_anomaly.set_source_anomalies([lhs, rhs])
                new_anomaly.set_source_node(self)
                return [new_anomaly]
            # Partial inclusion
            elif fst.end >= snd.start and fst.end <= snd.end:
                score = Slack.combined_scores(lhs, rhs)
                new_start = snd.start
                new_end = fst.end
                if new_start < new_end:
                    new_anomaly = Anomaly(new_start, fst.end, score)
                    new_anomaly.set_source_anomalies([lhs, rhs])
                    new_anomaly.set_source_node(self)
                    return [new_anomaly]
            else:
                return [lhs, rhs]

    @staticmethod
    def combined_scores(lhs, rhs):
        return (lhs.score + rhs.score)/2

    def get_params(self):
        slack = self.get_param('slack').value
        min_span = self.get_param('min_span').value
        return (slack, min_span)

    @staticmethod
    def validated_step(inputs):
        steps = []
        for i in inputs:
            steps.append(i.find_output_series().step())
        if len(np.unique(steps)) > 1:
            raise ValueError("All inputs must have same step size")
        return steps[0]

    def __str__(self):
        return 'Slack' + str(self.get_params()) + '[' + self.id + ']'

    def desc(self):
        return 'Extend anomalies and combine'

    def display(self):
        return 'Slack'
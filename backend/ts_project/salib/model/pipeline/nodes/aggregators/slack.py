import json
import numpy as np

from ..node import Node
from ..node_detector import NodeDetector
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
        self.add_required_param(String('min_gap', 'Min. gap', "Min. gap between anomalies (intervals or period, ej '3h'. Leave empty to ignore.", ''))

    def execute(self, inputs, debug):
        all_anomalies = []
        for i in inputs:
            all_anomalies += i.anomalies

        slack, min_span, min_gap = self.get_params()
        step = Slack.validated_step(inputs)
        if min_span == '' or min_span is None:
            calc_min_span = None
        else:
            calc_min_span = step * timedelta_to_period(min_span, step)
        if min_gap == '' or min_gap is None:
            calc_min_gap = None
        else:
            calc_min_gap = step * timedelta_to_period(min_gap, step)

        new_anomalies, debug_info = self.join(all_anomalies, slack, calc_min_span, calc_min_gap, debug)
        NodeDetector.normalize_anomalies(new_anomalies)
        return NodeResult(self, inputs=inputs, anomalies=new_anomalies, debug_info=debug_info)

    def join(self, all_anomalies, slack, min_span, min_gap, debug):
        all_anomalies_map = {}
        new_anomalies = []
        debug_info = {}

        side_slack = 0.01*(slack / 2)
        for anomaly in all_anomalies:
            all_anomalies_map[anomaly.id()] = anomaly
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
        new_anomalies = self.combine(new_anomalies, min_gap)
        # Remove intermediate anomaly references
        for anomaly in new_anomalies:
            new_source_anomalies = []
            for source_anomaly in anomaly.source_anomalies:
                new_source_anomalies += Slack.original_anomaly_references(source_anomaly, all_anomalies_map)
            new_source_anomalies = list(np.unique(new_source_anomalies))
            anomaly.set_source_anomalies(new_source_anomalies)

        # Debug info
        debug_info['start_anomaly_count'] = len(all_anomalies)
        debug_info['end_anomaly_count'] = len(new_anomalies)
        debug_info['anomaly_count_diff'] = debug_info['end_anomaly_count'] - debug_info['start_anomaly_count']

        return new_anomalies, debug_info

    @staticmethod
    def original_anomaly_references(anomaly, original_anomalies_map):
        result = []
        if anomaly.id() in original_anomalies_map:
            return [anomaly]
        else:
            children = [Slack.original_anomaly_references(a, original_anomalies_map) for a in anomaly.source_anomalies]
            for child in children:
                result += child
            return result

    def combine(self, anomalies, min_gap):
        if len(anomalies) <= 1:
            return anomalies
        else:
            last_result = list(np.sort(anomalies))
            iters = 0
            max_iters = 1000
            while True:
                # print("Before size anomalies %s (%s):" % (len(last_result),iters))
                new_result = []
                skip_next = False
                for_iter = 0
                for curr, nxt in zip(last_result, last_result[1:]):
                    # print(for_iter, curr.id(), nxt.id())
                    for_iter += 1
                    if skip_next:
                        skip_next = False
                        continue
                    # print("\nIter %s - Comparing pairs: %s-%s vs %s-%s: %s" % (iters, curr.start, curr.end, nxt.start, nxt.end, len(new_result)))
                    to_add = self.combine_pair(curr, nxt, min_gap)
                    if to_add is not None:
                        new_result.append(to_add)
                        skip_next = True
                    else:
                        new_result.append(curr)
                    # print("\nIter %s - Compared pairs: %s-%s vs %s-%s: %s" % (iters, curr.start, curr.end, nxt.start, nxt.end, len(new_result)))
                # Edge case add last unless merged
                if not skip_next:
                    new_result.append(last_result[-1])
                # print("All anomalies %s (%s):" % (len(new_result),iters))
                # for a in new_result:
                    # print("%s %s-%s" % (a.id(),a.start,a.end))
                if new_result == last_result:
                    break
                else:
                    last_result = new_result.copy()
                    if len(last_result) == 1:
                        break
                if iters > max_iters:
                    break
                else:
                    iters += 1
            return last_result

    def combine_pair(self, lhs, rhs, min_gap):
        if lhs.start == rhs.start and lhs.end == rhs.end:
            score = Slack.combined_scores(lhs, rhs)
            new_anomaly = Anomaly(lhs.start, lhs.end, score)
            new_anomaly.set_source_anomalies([lhs, rhs])
            new_anomaly.set_source_node(self)
            # print("\nCombining OK1: %s-%s vs %s-%s" % (lhs.start, lhs.end, rhs.start, rhs.end))
            return new_anomaly
        else:
            fst, snd = sorted((lhs,rhs))
            # Total inclusion
            if snd.start >= fst.start and snd.end <= fst.end:
                score = Slack.combined_scores(lhs, rhs)
                new_anomaly = Anomaly(fst.start, fst.end, score)
                new_anomaly.set_source_anomalies([lhs, rhs])
                new_anomaly.set_source_node(self)
                # print("\nCombining OK2: %s-%s vs %s-%s" % (fst.start, fst.end, snd.start, snd.end))
                return new_anomaly
            # Partial inclusion
            elif fst.end >= snd.start and fst.end <= snd.end:
                score = Slack.combined_scores(lhs, rhs)
                new_start = fst.start
                new_end = snd.end
                if new_start < new_end:
                    new_anomaly = Anomaly(new_start, new_end, score)
                    new_anomaly.set_source_anomalies([lhs, rhs])
                    new_anomaly.set_source_node(self)
                    # print("\nCombining OK3: %s-%s vs %s-%s" % (fst.start, fst.end, snd.start, snd.end))
                    return new_anomaly
                else:
                    raise ValueError('Zero span anomaly?')
            elif min_gap is not None and (snd.start - fst.end) < min_gap:
                score = Slack.combined_scores(lhs, rhs)
                new_anomaly = Anomaly(fst.start, snd.end, score)
                new_anomaly.set_source_anomalies([lhs, rhs])
                new_anomaly.set_source_node(self)
                # print("\nCombining OK4: %s-%s vs %s-%s" % (fst.start, fst.end, snd.start, snd.end))
                return new_anomaly
            else:
                # print("\nCombining failed: %s-%s vs %s-%s" % (fst.start, fst.end, snd.start, snd.end))
                return None

    @staticmethod
    def combined_scores(lhs, rhs):
        return (lhs.score + rhs.score)/2

    def get_params(self):
        slack = self.get_param('slack').value
        min_span = self.get_param('min_span').value
        min_gap = self.get_param('min_gap').value
        return (slack, min_span, min_gap)

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
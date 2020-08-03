import pandas as pd
from enum import IntEnum
from functools import total_ordering


class AnomalyType(IntEnum):
    ACTUAL_START = 0,
    ACTUAL_END = 1,
    EXPECTED_START = 2,
    EXPECTED_END = 3


@total_ordering
class TaggedAnomaly:

    def __init__(self, anomaly, anomaly_type, timestamp):
        self.anomaly = anomaly
        self.type = anomaly_type
        self.timestamp = timestamp

    def __eq__(self, other):
        return ((self.timestamp, self.type) == (other.timestamp, other.type))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return ((self.timestamp, self.type) < (other.timestamp, other.type))

    def __repr__(self):
        return str(self.type) + "[" + str(self.timestamp) + "]"


def build(series, expected_anomalies, actual_anomalies):

    tp = []
    fp = []
    tn = []
    fn = []

    start = series.start
    end = series.end

    assert_no_overlap(expected_anomalies)
    assert_no_overlap(actual_anomalies)

    anomalies_q = sorted_tagged_anomalies(expected_anomalies, actual_anomalies)

    last_pos = start
    current_expected = None
    current_actual = None

    while anomalies_q:
        next_anomaly = anomalies_q.pop(0)
        if next_anomaly.type == AnomalyType.ACTUAL_START:
            if current_actual is None and current_expected is None:
                tn.append([last_pos, next_anomaly.timestamp])
                last_pos = next_anomaly.timestamp
                current_actual = next_anomaly

        elif next_anomaly.type == AnomalyType.ACTUAL_END:
            if current_actual is not None and current_expected is not None:
                tp.append([last_pos, next_anomaly.timestamp])
                last_pos = next_anomaly.timestamp
                current_actual = None

        elif next_anomaly.type == AnomalyType.EXPECTED_START:
            if current_actual is not None and current_expected is None:
                fn.append([last_pos, next_anomaly.timestamp])
                last_pos = next_anomaly.timestamp
                current_expected = next_anomaly

        elif next_anomaly.type == AnomalyType.EXPECTED_END:
            if current_actual is None and current_expected is not None:
                fp.append([last_pos, next_anomaly.timestamp])
                last_pos = next_anomaly.timestamp
                current_expected = None

    # Edge cases on end

    return (tp, fp, tn, fn)


def sorted_tagged_anomalies(expected_anomalies, actual_anomalies):

    tagged_expected_anomalies = sum(map(
        lambda e:
            [TaggedAnomaly(e, AnomalyType.EXPECTED_START, e.start),
             TaggedAnomaly(e, AnomalyType.EXPECTED_END, e.end)],
        expected_anomalies), [])

    tagged_actual_anomalies = sum(map(
        lambda e:
            [TaggedAnomaly(e, AnomalyType.ACTUAL_START, e.start),
             TaggedAnomaly(e, AnomalyType.ACTUAL_END, e.end)],
        actual_anomalies), [])

    return sorted(list(tagged_actual_anomalies)
                  + list(tagged_expected_anomalies))


def assert_no_overlap(anomalies):
    sorted_anomalies = sorted(anomalies)
    if len(sorted_anomalies) == 0:
        return
    last_end = sorted_anomalies[0].end
    for anomaly in sorted_anomalies[1:]:
        if anomaly.start < last_end:
            raise Exception('Overlapping anomaly forbidden: ' + str(anomaly))
        last_end = anomaly.end


def interval_from_epochs(expected):
    return [
        pd.Timestamp(expected[0], unit='s'),
        pd.Timestamp(expected[1], unit='s')
    ]


def intervals_from_epochs(expected):
    return list(map(lambda e: interval_from_epochs(e), expected))

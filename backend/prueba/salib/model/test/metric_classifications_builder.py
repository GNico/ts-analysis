import pandas as pd
from enum import Enum


class Type(Enum):
    TP = 0,
    FP = 1,
    TN = 2,
    FN = 3


class AnomalyType(Enum):
    ACTUAL = 0,
    EXPECTED = 1


class TaggedAnomaly:

    def __init__(self, anomaly_type, anomaly):
        self.type = anomaly_type
        self.anomaly = anomaly


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

    # TODO
    while anomalies_q:
        peek_next = anomalies_q[0]
        break

    return (tp, fp, tn, fn)


def sorted_tagged_anomalies(expected_anomalies, actual_anomalies):

    tagged_expected_anomalies = map(
        lambda e: TaggedAnomaly(AnomalyType.EXPECTED, e),
        expected_anomalies)

    tagged_actual_anomalies = map(
        lambda e: TaggedAnomaly(AnomalyType.ACTUAL, e),
        actual_anomalies)

    return sorted(list(tagged_actual_anomalies)
                  + list(tagged_expected_anomalies),
                  key=lambda tagged_anomaly: tagged_anomaly.anomaly)


def assert_no_overlap(anomalies):
    sorted_anomalies = sorted(anomalies)
    if len(sorted_anomalies) == 0:
        return
    last_end = sorted_anomalies[0].end
    for anomaly in sorted_anomalies[1:]:
        if anomaly.start < last_end:
            raise Exception('Overlapping anomaly forbidden: ' + str(anomaly))
        last_end = anomaly.end


def interval_from_epoch(expected):
    return list(map(lambda e: [
        pd.Timestamp(e[0], unit='s'),
        pd.Timestamp(e[1], unit='s')
    ], expected))

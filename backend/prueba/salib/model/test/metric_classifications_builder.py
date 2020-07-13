from enum import Enum


class Type(Enum):
    TP = 0,
    FP = 1,
    TN = 2,
    FN = 3


def sorted_anomalies(anomalies):
    return sorted(anomalies)


def build(series, expected_anomalies, actual_anomalies):
    tp = []
    fp = []
    tn = []
    fn = []

    start = series.start
    end = series.end

    expected_q = sorted_anomalies(expected_anomalies)
    actual_q = sorted_anomalies(actual_anomalies)

    current_type = Type.TN
    current_pos = start

    # TODO

    return (tp, fp, tn, fn)

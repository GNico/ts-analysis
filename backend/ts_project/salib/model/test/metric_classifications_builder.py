import pandas as pd

def build(series, expected_anomalies, actual_anomalies):

    tp = []
    fp = []
    tn = []
    fn = []

    start = series.start
    end = series.end

    expected_anomalies = sorted(expected_anomalies)
    actual_anomalies = sorted(actual_anomalies)

    assert_no_overlap(expected_anomalies)
    assert_no_overlap(actual_anomalies)

    last_pos = start
    last_expected = None
    last_actual = None

    # TODO: optimize with bin-search?
    for i in range(start.second, end.second + 1):
        ts = pd.Timestamp(i, unit='s')
        is_actual = timestamp_included(ts, actual_anomalies)
        is_expected = timestamp_included(ts, expected_anomalies)
        if is_actual and is_expected:
            tp.append(ts)
        elif is_actual and not is_expected:
            fp.append(ts)
        elif not is_actual and not is_expected:
            tn.append(ts)
        elif not is_actual and is_expected:
            fn.append(ts)

    return (tp, fp, tn, fn)


def timestamp_included(ts, anomalies):
    for anom in anomalies:
        if ts >= anom.start and ts <= anom.end:
            return True
    return False

def assert_no_overlap(sorted_anomalies):
    if len(sorted_anomalies) == 0:
        return
    last_end = sorted_anomalies[0].end
    for anomaly in sorted_anomalies[1:]:
        if anomaly.start < last_end:
            raise Exception('Overlapping anomaly forbidden: ' + str(anomaly))
        last_end = anomaly.end


def epochs_to_timestamp(epochs):
    return list(map(lambda e: pd.Timestamp(e, unit='s'), epochs))
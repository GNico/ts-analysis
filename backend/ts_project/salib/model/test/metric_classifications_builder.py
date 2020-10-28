import pandas as pd


def build(series, expected_anomalies, actual_anomalies):

    expected_anomalies = sorted(expected_anomalies)
    actual_anomalies = sorted(actual_anomalies)

    assert_no_overlap(expected_anomalies)
    assert_no_overlap(actual_anomalies)

    singles = {}
    singles['tp'] = []
    singles['fp'] = []
    singles['tn'] = []
    singles['fn'] = []
    ranges = {}
    ranges['tp'] = []
    ranges['fp'] = []
    ranges['fn'] = []
    ranges['tn'] = []
    # TODO: optimize with bin-search?
    last_ts = None
    start_ts = None
    last_type = None

    for ts in series.pdseries.index:
        is_actual = timestamp_included(ts, actual_anomalies)
        is_expected = timestamp_included(ts, expected_anomalies)

        if is_actual and is_expected:
            type = 'tp'
        elif is_actual and not is_expected:
            type = 'fp'
        elif not is_actual and not is_expected:
            type = 'tn'
        elif not is_actual and is_expected:
            type = 'fn'

        singles[type].append(ts)

        if last_type is None:
            last_type = type
            start_ts = ts

        if last_type != type:
            ranges[last_type].append([start_ts, last_ts])
            start_ts = ts
            last_type = type
        last_ts = ts

    ranges[last_type].append([start_ts, last_ts])

    return (ranges['tp'], ranges['fp'], ranges['fn'], ranges['tn'],
            singles['tp'], singles['fp'], singles['tn'], singles['fn'])


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


def epochs_to_ranges(epochs):
    return list(map(lambda e:
                [pd.Timestamp(e[0], unit='s'), pd.Timestamp(e[1], unit='s')],
                epochs))

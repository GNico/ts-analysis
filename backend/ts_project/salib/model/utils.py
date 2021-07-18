import math
import pandas as pd

def timestamp_to_epoch(timestamp):
    return timestamp.value // int(1e6)

def timestamp_to_epoch_secs(timestamp):
    return timestamp.value // int(1e9)

def timedelta_to_period(period_str, base_period, validate=True):
    try:
        return int(period_str)
    except ValueError:
        period = pd.Timedelta(period_str)
        frac = period / base_period
        if validate and frac < 1 and frac > -1:
            raise ValueError('Period cannot be smaller than base period')
        else:
            return math.floor(frac)

def lags_range_timedelta_to_period(str_spec, base_period, validate=True):
    parts = list(map(lambda e: e.strip(), str_spec.split(',')))
    result = []
    for part in parts:
        is_range = part.count('-') == 1
        if is_range:
            start, end = list(map(lambda e: timedelta_to_period(e.strip(), base_period), part.split('-')))
            result += list(range(start, end+1))
        else:
            if len(parts) == 1:
                end = timedelta_to_period(part, base_period)
                result += list(range(0, end+1))
            else:
                result.append(timedelta_to_period(part, base_period))
    if len(result) > 1 and 0 in result:
        result.remove(0)
    return result
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
import math
import pandas as pd

def timestamp_to_epoch(timestamp):
    return (timestamp - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')

def timestamp_to_epoch_secs(timestamp):
    return (timestamp - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

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
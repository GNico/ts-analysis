import pandas as pd


def timestamp_to_epoch(timestamp):
    return (timestamp - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

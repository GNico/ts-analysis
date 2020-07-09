import pandas as pd


class Series:

    def __init__(self, pdseries, interval):
        self.pdseries = pdseries
        self.start = pdseries[0]
        self.end = pdseries[-1]
        self.interval = interval

    def fromArray(arr, interval):
        dates, count = zip(*arr)
        dates = pd.to_datetime(dates, unit='ms')
        return Series(pd.Series(count, index=dates), interval)

import pandas as pd


class Series:

    def __init__(self, pdseries, interval):
        self.pdseries = pdseries
        self.start = pdseries.index[0]
        self.end = pdseries.index[-1]
        self.interval = interval

    def from_array(arr, interval, unit='ms'):
        dates, count = zip(*arr)
        dates = pd.to_datetime(dates, unit=unit)
        return Series(pd.Series(count, index=dates), interval)

    def __str__(self):
        return 'Series [' + str(self.start) + ' to ' + str(self.end) + ']' \
                ' (' + str(self.interval) + ')'

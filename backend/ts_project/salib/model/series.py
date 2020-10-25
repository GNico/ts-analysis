import pandas as pd
from .utils import timestamp_to_epoch


class Series:

    def __init__(self, pdseries, interval):
        self.pdseries = pdseries
        self.start = pdseries.index[0]
        self.end = pdseries.index[-1]
        self.interval = interval

    def span(self):
        return len(self.pdseries.index)

    def time_idx(self, timestamp):
        # ToDo optimize
        for i in range(0, self.span()):
            if self.pdseries.index[i] == timestamp:
                return i
        return None

    def from_array(arr, interval, unit='s'):
        dates, count = zip(*arr)
        dates = pd.to_datetime(dates, unit=unit)
        return Series(pd.Series(count, index=dates), interval)

    def __str__(self):
        return 'Series [' + str(self.start) + ' to ' + str(self.end) + ']' \
                ' (' + str(self.interval) + ')'

    def as_list(self):
        return list(self.pdseries.values)

    def output_format(self):
        output = []
        for i in range(0, self.span()):
            output.append(
                [timestamp_to_epoch(self.pdseries.index[i]),
                 int(self.pdseries[i])])
        return output

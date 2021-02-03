import pandas as pd
from .utils import timestamp_to_epoch


class Series:

    def __init__(self, pdseries, interval=None):
        self.pdseries = pdseries
        if len(pdseries.index) < 2:
            raise RuntimeError("Series must contain 2 or more data points!")
        self.start = pdseries.index[0]
        self.end = pdseries.index[-1]
        if interval is None:
            self.interval = self.calculate_interval()
        else:
            self.interval = interval

    def calculate_interval(self):
        series = self.pdseries
        if not (series.index.is_monotonic_increasing or series.index.is_monotonic_decreasing):
            raise ValueError('Index must be monotonic')
        # ToDo validate equal spaced indices, taking first two points for now
        return series.index[1] - series.index[0]

    def span(self):
        return len(self.pdseries.index)

    def time_idx(self, timestamp):
        # ToDo optimize
        for i in range(0, self.span()):
            if self.pdseries.index[i] == timestamp:
                return i
        return None

    @staticmethod
    def from_array(arr, interval, unit='s'):
        dates, count = zip(*arr)
        dates = pd.to_datetime(dates, unit=unit)
        return Series(pd.Series(count, index=dates), pd.to_timedelta(interval, unit='s'))

    def __str__(self):
        return 'Series [' + str(self.start) + ' to ' + str(self.end) + ']' \
                ' (' + str(self.interval) + ')'

    def as_list(self):
        return list(self.pdseries.values)

    def step(self):
        return self.interval

    def end_bound(self):
        return self.end + self.step()

    def output_format(self):
        output = []
        for i in range(0, self.span()):
            output.append(
                [timestamp_to_epoch(self.pdseries.index[i]),
                 int(self.pdseries[i])])
        return output

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset

from .utils import timestamp_to_epoch

class Series:

    def __init__(self, pdseries):
        self.pdseries = pdseries
        if len(pdseries.index) < 2:
            raise RuntimeError("Series must contain 2 or more data points!")
        self.start = pdseries.index[0]
        self.end = pdseries.index[-1]
        self.interval = self.calculate_interval()

    def calculate_interval(self):
        series = self.pdseries
        if not (series.index.is_monotonic_increasing or series.index.is_monotonic_decreasing):
            raise ValueError('Index must be monotonic')
        if len(series.index) == 2:
            series.index.freq = to_offset(series.index[1]-series.index[0])
        if series.index.freq is None:
            if series.index.inferred_freq is None:
                deltas, counts = np.unique(pd.Series(series.index).diff(1).dropna().values, return_counts=True)
                frequencies = list(zip(deltas, counts))
                raise ValueError('Index must be equally spaced, could not infer frequency\nIndex: %s\nDeltas: %s' % (series.index, frequencies))
            series.index.freq = series.index.inferred_freq
        return series.index.freq.delta

    def span(self):
        return len(self.pdseries.index)

    def time_idx(self, timestamp):
        # ToDo optimize
        for i in range(0, self.span()):
            if self.pdseries.index[i] == timestamp:
                return i
        return None

    @staticmethod
    def from_array(arr, unit='s'):
        dates, count = zip(*arr)
        dates = pd.to_datetime(dates, unit=unit)
        return Series(pd.Series(count, index=dates))

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
        return [[timestamp_to_epoch(i[0]),float(i[1])] for i in self.pdseries.items()]

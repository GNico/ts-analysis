import numpy as np
from ..anomaly import Anomaly
from ..baseline import Baseline


class EMA:

    def __init__(self, decay, threshold):
        self.decay = decay
        self.threshold = threshold

    def anomalies(self, series):
        return self.do(series)[0]

    def baseline(self, series):
        return self.do(series)[1]

    def do(self, series):
        anomalies = []
        baseline = Baseline()
        pdseries = series.pdseries
        min_periods = self.decay*10
        ema = pdseries.ewm(com=self.decay, min_periods=min_periods)
        ema = ema.mean().dropna()
        diffs = []
        for val in ema.items():
            ema_val = val[1]
            series_val = pdseries[val[0]]
            diff = abs(series_val - ema_val)
            diffs.append(diff)
            # print(val[0], series_val, ema_val, diff)
        diffs_mean = np.mean(diffs, axis=0)
        diffs_std = np.std(diffs, axis=0)
        # print("Diffs mean", diffs_mean)
        # print("Diffs std", diffs_std)
        start = None
        for val in ema.items():
            ema_val = val[1]
            series_val = pdseries[val[0]]
            diff = abs(series_val - ema_val)
            std_high = diffs_mean + self.threshold*diffs_std
            std_low = diffs_mean - self.threshold*diffs_std
            within_std_high = diff < std_high
            within_std_low = diff > std_low
            baseline.add_point(val[0], std_low, std_high)
            within_std = within_std_high and within_std_low
            if not within_std and start is None:
                start = val[0]
            elif within_std and start is not None:
                score = 1.0  # ToDo
                new_anomaly = Anomaly(series, start, val[0], score)
                anomalies.append(new_anomaly)
                start = None
        return (anomalies, baseline)

    def id(self):
        return "EMA(" + str(self.decay) + "," + str(self.threshold) + ")"

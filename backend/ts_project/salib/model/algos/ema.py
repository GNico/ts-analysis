import numpy as np
from ..anomaly import Anomaly


class EMA:

    def __init__(self, decay, threshold):
        self.decay = decay
        self.threshold = threshold

    def anomalies(self, series):
        anomalies = []
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
            within_std_l = diff < (diffs_mean + self.threshold*diffs_std)
            within_std_r = diff > (diffs_mean - self.threshold*diffs_std)
            within_std = within_std_l and within_std_r
            if not within_std and start is None:
                start = val[0]
            elif within_std and start is not None:
                score = 1.0  # ToDo
                new_anomaly = Anomaly(start, val[0], score)
                anomalies.append(new_anomaly)
                start = None
        return anomalies

    def id(self):
        return "EMA(" + str(self.decay) + "," + str(self.threshold) + ")"

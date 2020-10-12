from .analysis import Analysis
from .algos.no_trend import NoTrend
from .algos.no_baseline import NoBaseline


class Analyzer:

    def __init__(self, anomalies_algos,
                 trend_algo=NoTrend(),
                 baseline_algo=NoBaseline(),
                 config={}):
        self.anomalies_algos = anomalies_algos
        self.trend_algo = trend_algo
        self.baseline_algo = baseline_algo
        self.config = config

    def analyze(self, series):

        all_anomalies = []
        for algo in self.anomalies_algos:
            anomalies = algo.anomalies(series)
            for anomaly in anomalies:
                anomaly.tag_algo(algo.id())
            all_anomalies.extend(anomalies)

        trend = self.trend_algo.trend(series)
        baseline = self.baseline_algo.baseline(series)
        return Analysis(all_anomalies, trend, baseline)

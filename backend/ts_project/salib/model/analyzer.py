from .analysis import Analysis
from .algos.mock import NoBaseline


class Analyzer:

    def __init__(self, anomalies_algos,
                 baseline_algo=NoBaseline(),
                 config={}):
        self.anomalies_algos = anomalies_algos
        self.baseline_algo = baseline_algo
        self.config = config

    def analyze(self, series):

        all_anomalies = []
        for algo in self.anomalies_algos:
            anomalies = algo.anomalies(series)
            for anomaly in anomalies:
                anomaly.tag_algo(algo.id())
            all_anomalies.extend(anomalies)

        baseline = self.baseline_algo.baseline(series)
        return Analysis(all_anomalies, baseline)

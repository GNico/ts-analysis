class Analysis:

    def __init__(self, anomalies, baseline):
        self.anomalies = anomalies
        self.build_anomalies_map()
        self.baseline = baseline

    def anomalies_by_algo(self):
        return self.anomalies_by_algo

    def build_anomalies_map(self):
        self.anomalies_by_algo = {}
        for anomaly in self.anomalies:
            algo_id = anomaly.algo_tag
            if algo_id not in self.anomalies_by_algo:
                self.anomalies_by_algo[algo_id] = []
            self.anomalies_by_algo[algo_id].append(anomaly)

    def output_format(self):
        anomalies = list(map(lambda a: a.output_format(), self.anomalies))
        baseline = self.baseline.output_format()
        return {
            "anomalies": anomalies,
            "baseline": baseline
        }

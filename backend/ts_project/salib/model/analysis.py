class Analysis:

    def __init__(self, series, anomalies, baseline):
        self.series = series
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
        series = self.series.output_format()
        anomalies = list(map(lambda a: a.output_format(), self.anomalies))
        baseline = self.baseline.output_format()
        return {
            "series": series,
            "anomalies": anomalies,
            "baseline": baseline
        }

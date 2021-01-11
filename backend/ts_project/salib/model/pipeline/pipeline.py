class Pipeline:

    def __init__(self, algos):
        self.algos = algos

    def execute(self, series):
        all_anomalies = []
        # ToDo improve with AND/OR logic
        # For now it's all OR
        for algo in self.algos:
            anomalies = algo.anomalies(series)
            for anomaly in anomalies:
                anomaly.tag_algo(algo.id())
            all_anomalies.extend(anomalies)
        return all_anomalies
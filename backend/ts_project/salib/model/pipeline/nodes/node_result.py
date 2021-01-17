class NodeResult:

    def __init__(self, source_node, series=None, anomalies=[]):
        self.node = source_node
        self.series = series
        self.anomalies = anomalies

    def set_series(self, series):
        self.series = series

    def add_anomalies(self, anomalies):
        self.anomalies.extend(anomalies)
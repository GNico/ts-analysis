class NodeResult:

    def __init__(self, source_node, inputs, series=None, anomalies=[]):
        self.node = source_node
        if self.node is None:
            self.id = None
        else:
            self.id = self.node.id
        self.series = series
        self.anomalies = anomalies
        self.inputs = inputs

    def set_series(self, series):
        self.series = series

    def add_anomalies(self, anomalies):
        self.anomalies.extend(anomalies)

    def find_node(self, id):
        if self.id == id:
            return self
        else:
            match = None
            for input in self.inputs:
                match = input.find_node(x)
                if match is not None:
                    break
            return match
        return None
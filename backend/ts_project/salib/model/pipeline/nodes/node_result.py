class NodeResult:

    def __init__(self, source_node, inputs, output_series=None, anomalies=[]):
        self.node = source_node
        if self.node is None:
            self.id = None
        else:
            self.id = self.node.id
        self.output_series = output_series
        self.anomalies = anomalies
        self.inputs = inputs

    def set_output_series(self, output_series):
        self.output_series = output_series

    def add_anomalies(self, anomalies):
        self.anomalies.extend(anomalies)

    def find_output_series(self):
        if self.output_series is not None:
            return self.output_series
        else:
            # Should be single input when going up the detector chain
            # Until we find a transformer or input
            return self.inputs[0].find_output_series()

    def display_series(self):
        if self.output_series is not None:
            return {"output": self.output_series}
        else:
            input_names = self.node.input_names
            if len(input_names) == 0:
                res = {}
                idx = 1
                for input in self.inputs:
                    res[("input_%s" % idx)] = input.find_output_series()
                    idx += 1
                return res
            else:
                idx = 0
                res = {}
                for input in self.inputs:
                    res[input_names[idx]] = input.find_output_series()
                    idx += 1
                return res

    def all_sources(self, acc=[]):
        for input in self.inputs:
            acc.append(input)
            input.all_sources(acc)
        return acc

    def find_node(self, id):
        if self.id == id:
            return self
        else:
            match = None
            for input in self.inputs:
                match = input.find_node(id)
                if match is not None:
                    break
            return match
        return None
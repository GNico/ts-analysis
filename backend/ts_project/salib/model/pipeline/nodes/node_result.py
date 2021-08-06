class NodeResult:

    def __init__(self, source_node, inputs, output_series=None, anomalies=[], debug_info={}):
        self.node = source_node
        if self.node is None:
            self.id = None
        else:
            self.id = self.node.id
        self.output_series = output_series
        self.anomalies = anomalies
        self.inputs = inputs
        self.debug_info = debug_info

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

    def output_format(self):
        return {
            "series": {k: v.output_format() for k, v in self.display_series().items()},
            "anomalies": list(map(lambda a: a.output_format(), self.anomalies)),
            "debug_info": {} if self.debug_info is None else {k: NodeResult.pretty_debug_info(v) for k, v in self.debug_info.items()}
        }

    @staticmethod
    def pretty_debug_info(node_element):
        if isinstance(node_element, float):
            return round(node_element, 3)
        else:
            return node_element

    def all_sources(self):
        ret = []
        self.all_sources_rec(ret)
        return ret

    def all_sources_rec(self, acc):
        for input in self.inputs:
            acc.append(input)
            input.all_sources_rec(acc)

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
import pandas as pd

class Analysis:

    def __init__(self, inputs, result, anomalies, debug):
        self.inputs = inputs
        self.result = result
        self.anomalies = anomalies
        self.debug = debug
        self.build_anomalies_map()

    def anomalies_by_node(self):
        return self.anomalies_by_node

    def result_for_node(self, id):
        return self.result.find_node(id)

    def build_anomalies_map(self):
        self.anomalies_by_node = {}
        for anomaly in self.anomalies:
            if anomaly.source_node is None:
                continue
            source_node_id = anomaly.source_node.id
            if source_node_id not in self.anomalies_by_node:
                self.anomalies_by_node[source_node_id] = []
            self.anomalies_by_node[source_node_id].append(anomaly)

    def output_format(self):
        inputs = {k: v.output_format() for k, v in self.inputs.items()}
        anomalies = list(map(lambda a: a.output_format(), self.anomalies))

        result = {
            "series": inputs,
            "anomalies": anomalies,
        }

        if self.debug:
            result["debug_nodes"] = self.debug_nodes_output()

        return result

    def debug_nodes_output(self):
        all_sources = self.result.all_sources()
        debug_nodes_output = {}
        for debug_node in all_sources:
            if debug_node.id is not None:
                debug_nodes_output[debug_node.id] = debug_node.output_format()
        return debug_nodes_output

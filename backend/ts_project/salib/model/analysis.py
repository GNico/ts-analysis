class Analysis:

    def __init__(self, series, result, anomalies):
        self.series = series
        self.result = result
        self.anomalies = anomalies
        self.build_anomalies_map()

    def anomalies_by_node(self):
        return self.anomalies_by_node

    def result_for_node(self, id):
        return self.result.find_node(id)

    def result_debug_nodes(self):
        debug_nodes = []
        self.result.debug_nodes(debug_nodes)
        return debug_nodes

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
        series = self.series.output_format()
        anomalies = list(map(lambda a: a.output_format(), self.anomalies))
        
        debug_nodes = self.result_debug_nodes()
        debug_nodes_output = {}
        for debug_node in debug_nodes:
            debug_nodes_output[debug_node.id] = {
                "series": debug_node.series.output_format(),
                "anomalies": list(map(lambda a: a.output_format(), debug_node.anomalies))
            }

        return {
            "series": series,
            "anomalies": anomalies,
            "debug_nodes": debug_nodes_output,
        }

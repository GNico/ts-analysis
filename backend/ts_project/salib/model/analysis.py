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
            result["anomalies_histograms"] = self.build_anomalies_histograms()
            result["anomalies_heatmaps"] = self.build_anomalies_heatmaps()

        return result

    def debug_nodes_output(self):
        all_sources = self.result.all_sources()
        debug_nodes_output = {}
        for debug_node in all_sources:
            if debug_node.id is not None:
                debug_nodes_output[debug_node.id] = debug_node.output_format()
        return debug_nodes_output

    def build_anomalies_histograms(self):
        heatmaps = []
        heatmaps.append(self.build_anomalies_histogram('Day of week', lambda i: i.dayofweek, 24,
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
        heatmaps.append(self.build_anomalies_histogram('Month of year', lambda i: i.month, 730,
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dic']))
        heatmaps.append(self.build_anomalies_histogram('Hour of day', lambda i: i.hour, 1,
            [str(h) for h in range(0, 24)]))
        heatmaps.append(self.build_anomalies_histogram('Day of month', lambda i: i.day, 24,
            [str(h) for h in range(0, 32)]))
        return heatmaps

    def build_anomalies_histogram(self, desc, idxfunc, period, labels):
        heatmap = {}
        heatmap['desc'] = desc
        heatmap['labels'] = labels
        counts = [0] * len(labels)
        for anomaly in self.anomalies:
            freq_str_h = str(period) + 'H'
            min_delta = pd.Timedelta(freq_str_h)
            if anomaly.span() <= min_delta:
                index = [anomaly.start]
            else:
                index = pd.date_range(anomaly.start, anomaly.end, freq=freq_str_h, closed='left')
            for i in index:
                counts[idxfunc(i)] += 1
        heatmap['data'] = [list(z) for z in zip(range(0, len(labels)), counts)]
        return heatmap

    def build_anomalies_heatmaps(self):
        heatmaps = []
        heatmaps.append(self.build_anomalies_heatmap('Hour of day/Day of week',
            lambda i: i.hour, 1,[str(h) for h in range(0, 24)],
            lambda i: i.dayofweek, 24, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
        heatmaps.append(self.build_anomalies_heatmap('Day of month/Day of week',
            lambda i: i.day, 24, [str(h) for h in range(0, 32)],
            lambda i: i.dayofweek, 24, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
        heatmaps.append(self.build_anomalies_heatmap('Day of month/Month of year',
            lambda i: i.day, 24, [str(h) for h in range(0, 32)],
            lambda i: i.dayofweek, 24, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
        return heatmaps

    def build_anomalies_heatmap(self, desc, idxfunc_x, period_x, labels_x, idxfunc_y, period_y, labels_y):
        heatmap = {}
        heatmap['desc'] = desc
        heatmap['labels_x'] = labels_x
        heatmap['labels_y'] = labels_y
        # Init zero counts
        counts = {}
        for x in range(len(labels_x)):
            for y in range(len(labels_y)):
                counts[(x,y)] = 0
        # Calc values
        for anomaly in self.anomalies:
            freq_str_h_x = str(period_x) + 'H'
            min_delta_x = pd.Timedelta(freq_str_h_x)
            if anomaly.span() <= min_delta_x:
                indices_x = [anomaly.start]
            else:
                indices_x = pd.date_range(anomaly.start, anomaly.end, freq=freq_str_h_x, closed='left')
            for x in indices_x:
                freq_str_h_y = str(period_y) + 'H'
                min_delta_y = pd.Timedelta(freq_str_h_y)
                if anomaly.span() <= min_delta_y:
                    indices_y = [anomaly.start]
                else:
                    indices_y = pd.date_range(anomaly.start, anomaly.end, freq=freq_str_h_y, closed='left')
                for y in indices_y:
                    counts[(idxfunc_x(x),idxfunc_y(y))] += 1
        output_data = []
        for k, v in counts.items():
            output_data.append([k[0], k[1], v])
        heatmap['data'] = output_data
        return heatmap

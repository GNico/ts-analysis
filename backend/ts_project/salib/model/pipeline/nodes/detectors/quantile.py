from ..node_detector import NodeDetector
from ...params.float import BoundedFloat

class Quantile(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(BoundedFloat('high', 'Quantile upper', 'Quantile above which we consider anomaly (0-1) - leave empty for no limit', 0, 1, False, 0.9))
        self.add_required_param(BoundedFloat('low', 'Quantile lower', 'Quantile below which we consider anomaly (0-1) - leave empty for no limit', 0, 1, False, 0.1))

    def anomalies(self, input):
        abs_low, abs_high = self.get_thresholds(input.series)
        return NodeDetector.from_filtered_values(input.series, filtered_series)

    def get_thresholds(self, series):
        s = series.pdseries
        if s.count() == 0:
            raise RuntimeError("Series does not have enough values")
        
        low, high = self.get_param_values()
        if high is None:
            abs_high = float("inf")
        else:
            abs_high = s.quantile(high)
        if low is None:
            abs_low = -float("inf")
        else:
            abs_low = s.quantile(low)
        return (abs_low, abs_high)

    def valid_threshold(self, abs_low, abs_high, val):
        return val > abs_high or val < abs_low

    def get_param_values(self):
        high = self.get_param('high').value
        low = self.get_param('low').value
        return low, high

    def __str__(self):
        return "Quantile(%s,%s)[%s]" % (self.get_param_values() + (self.id,))

    def display(self):
        return 'Quantile'

    def desc(self):
        return 'Compare values with given quantiles and identify anomalies beyond inter-quantile range'

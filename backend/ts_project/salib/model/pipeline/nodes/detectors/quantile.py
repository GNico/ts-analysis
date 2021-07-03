from ..node_detector import NodeDetector
from ...params.float import BoundedFloat

class Quantile(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_param(BoundedFloat('high', 'Quantile upper %', 'Quantile above which we consider anomaly (%) - leave empty for no limit', 0, 100, False, 90))
        self.add_param(BoundedFloat('low', 'Quantile lower %', 'Quantile below which we consider anomaly (%) - leave empty for no limit', 0, 100, False, 0))

    def anomalies(self, input_series):
        lo_bound, hi_bound = self.compute_thresholds(input_series)
        def predicate(val):
            return (hi_bound is not None and val > hi_bound) or (lo_bound is not None and val < lo_bound)
        # import pdb; pdb.set_trace()
        return NodeDetector.pointwise_consecutive(predicate, input_series)

    def compute_thresholds(self, series):
        s = series.pdseries
        if s.count() == 0:
            raise RuntimeError("Series does not have enough values")
        
        low, high = self.get_param_values()
        if high is not None:
            high = s.quantile(high*0.01)
        if low is not None:
            low = s.quantile(low*0.01)
        return (low, high)

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

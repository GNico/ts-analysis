from ..node_detector import NodeDetector
from ...params.float import BoundedFloat
from ...params.boolean import Boolean
from .simple_threshold import SimpleThreshold

class Quantile(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_param(BoundedFloat('upper', 'Quantile upper %', 'Quantile upper bound (%) - leave empty for no limit', 0, 100, False, 90))
        self.add_param(BoundedFloat('lower', 'Quantile lower %', 'Quantile lower bound (%) - leave empty for no limit', 0, 100, False, 0))
        self.add_required_param(Boolean('inside', 'Inside', 'If true, value must be within bounds', False))
        self.add_required_param(Boolean('strict', 'Strict', 'Strict comparison on bounds', True))

    def anomalies(self, input_series, debug):
        lower, upper, inside, strict = self.get_params()

        lo_bound, hi_bound = self.compute_thresholds(input_series, lower, upper)

        anomaly_score = SimpleThreshold.threshold_func(inside, strict, lo_bound, hi_bound)
        return (NodeDetector.pointwise_consecutive(anomaly_score, input_series), {})

    def compute_thresholds(self, series, lower, upper):
        s = series.pdseries
        if s.count() == 0:
            raise RuntimeError("Series does not have enough values")
        
        if lower is not None:
            lower = s.quantile(lower*0.01)
        if upper is not None:
            upper = s.quantile(upper*0.01)

        return (lower, upper)

    def get_params(self):
        lower = self.get_param('lower').value
        upper = self.get_param('upper').value
        inside = self.get_param('inside').value
        strict = self.get_param('strict').value
        return (lower, upper, inside, strict)

    def __str__(self):
        get_params = [str(x) for x in self.get_params()] + [self.id]
        return "Quantile(%s,%s,%s,%s)[%s]" % tuple(get_params)

    def display(self):
        return 'Quantile'

    def desc(self):
        return 'Compare values with given quantiles and identify anomalies beyond inter-quantile range'

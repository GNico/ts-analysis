from ..node_detector import NodeDetector
from ...params.float import Float
from ...params.boolean import Boolean

class SimpleThreshold(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('inside', 'Inside', 'If true, value must be within bounds', False))
        self.add_required_param(Boolean('strict', 'Strict', 'Strict comparison on bounds', False))
        self.add_param(Float('lower', 'Lower', 'Lower bound'))
        self.add_param(Float('upper', 'Upper', 'Upper bound'))

    def anomalies(self, input_series, debug):
        return (NodeDetector.pointwise_consecutive(self.anomaly_threshold(), input_series), {})

    def anomaly_threshold(self):
        lower, upper, inside, strict = self.get_params()
        return SimpleThreshold.threshold_func(inside, strict, lower, upper)

    @staticmethod
    def threshold_func(inside, strict, lower, upper):
        def threshold_func_eval(val):
            if inside:
                if upper is not None and lower is not None:
                    if (strict and val < upper and val > lower) or (not strict and val <= upper and val >= lower):
                        midpoint = (upper - lower / 2) + lower
                        return abs(val - midpoint)
                    else:
                        return None
                elif upper is not None:
                    if (strict and val < upper) or (not strict and val <= upper):
                        return upper - val
                    else:
                        return None
                elif lower is not None:
                    if (strict and val > lower) or (not strict and val >= lower):
                        return val - lower
                    else:
                        return None
                else:
                    return None
            else:
                if upper is not None:
                    if (strict and val > upper) or (not strict and val >= upper):
                        return val - upper
                if lower is not None:
                    if (strict and val < lower) or (not strict and val <= lower):
                        return lower - val
                return None
        return threshold_func_eval

    def get_params(self):
        lower = self.get_param('lower').value
        upper = self.get_param('upper').value
        inside = self.get_param('inside').value
        strict = self.get_param('strict').value
        return (lower, upper, inside, strict)

    def __str__(self):
        get_params = [str(x) for x in self.get_params()] + [self.id]
        return "SimpleThreshold(%s,%s,%s,%s)[%s]" % tuple(get_params)

    def display(self):
        return 'Simple Threshold'

    def desc(self):
        return 'Detect values outside of bounds'

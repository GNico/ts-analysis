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

    def anomalies(self, input):
        return NodeDetector.pointwise_consecutive(self.valid_threshold, input.output_series)

    def valid_threshold(self, val):
        lower, upper, inside, strict = self.all_params()
        if not strict.value and ((upper.is_set() and upper.value == val) or (lower.is_set() and lower.value == val)):
            return True
        if inside.value:
            req_upper = not upper.is_set() or val < upper.value
            req_lower = not lower.is_set() or val > lower.value
            return req_upper and req_lower
        else:
            req_upper = upper.is_set() and val > upper.value
            req_lower = lower.is_set() and val < lower.value
            return req_upper or req_lower

    def all_params(self):
        lower = self.get_param('lower')
        upper = self.get_param('upper')
        inside = self.get_param('inside')
        strict = self.get_param('strict')
        return (lower, upper, inside, strict)

    def __str__(self):
        all_params = [str(x.value) for x in self.all_params()] + [self.id]
        return "SimpleThreshold(%s,%s,%s,%s)[%s]" % tuple(all_params)

    def display(self):
        return 'Simple Threshold'

    def desc(self):
        return 'Detect values outside of bounds'

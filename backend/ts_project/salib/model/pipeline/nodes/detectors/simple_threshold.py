from ..node_detector import NodeDetector
from ...params.float import Float
from ...params.boolean import Boolean
from ....anomaly import Anomaly

class SimpleThreshold(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('inside', 'Inside', 'If true, value must be within bounds', False))
        self.add_param(Float('below', 'Below', 'Below threshold'))
        self.add_param(Float('above', 'Above', 'Above threshold'))

    def anomalies(self, input):
        print("Running",str(self))
        series = input.series
        pdseries = series.pdseries
        anomalies = []

        current_start = None
        for elem in pdseries.items():
            if self.valid_threshold(elem[1]):
                if current_start is None:
                    current_start = elem[0]
            else:
                if current_start is not None:
                    # TODO: calculate score
                    anomaly = Anomaly(series, current_start, elem[0], 1.0)
                    anomalies.append(anomaly)
                    current_start = None

        if current_start is not None:
            # TODO: calculate score
            anomaly = Anomaly(series, current_start, series.end_bound(), 1.0)
            anomalies.append(anomaly)

        return anomalies

    def valid_threshold(self, val):
        below, above, inside = self.all_params()
        if not inside.value:
            req_above = above.is_set() and val >= above.value
            req_below = below.is_set() and val <= below.value
            return req_above or req_below
        else:
            req_above = not above.is_set() or val <= above.value
            req_below = not below.is_set() or val >= below.value
            return req_above and req_below

    def all_params(self):
        below = self.get_param('below')
        above = self.get_param('above')
        inside = self.get_param('inside')
        return (below, above, inside)

    def __str__(self):
        all_params = [str(x.value) for x in self.all_params()] + [self.id]
        return "SimpleThreshold(%s,%s,%s)[%s]" % tuple(all_params)

    def display(self):
        return 'Simple Threshold'

    def desc(self):
        return 'Detect values outside of bounds'

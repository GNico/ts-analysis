from ..node_detector import NodeDetector
from ...params.float import Float

class InterQuartileRange(NodeDetector):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Float('scale', 'Range scale factor', 'Factor used to determine the bound of normal range (betweeen Q1-c*IQR and Q3+c*IQR)', 0.3))

    def anomalies(self, input_series):
        # WIP, TODO
        abs_low, abs_high = self.get_thresholds(input_series)
        return NodeDetector.pointwise_consecutive(self.valid_threshold, input_series)

    def get_thresholds(self, series):
        c = self.get_param('scale').value
        s = series.pdseries
        if s.count() == 0:
            raise RuntimeError("Series does not have enough values")
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        abs_low_ = q1 - (iqr * c)
        abs_high = q3 + (iqr * c)
        return (abs_low, abs_high)

    def valid_threshold(self, abs_low, abs_high, val):
        return val > abs_high or val < abs_low

    def __str__(self):
        return "InterQuartileRange(%s)[%s]" % (self.get_param('scale').value, self.id)

    def display(self):
        return 'Inter-quartile range'

    def desc(self):
        return 'Compare values with 1st and 3rd quartiles and identify anomalies beyond inter-quartile range adjusted by a scale factor'

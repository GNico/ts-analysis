from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption

from ....utils import timedelta_to_period

class ExponentialSmoothing(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('span', 'Span', 'Span size in time interval (eg: 12h)', '12h'))
        agg_method_options = [
            SelectOption("mean", "Mean"),
            SelectOption("std", "Sample standard dev."),
            SelectOption("var", "Sample variance"),
        ]
        self.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        
        span, agg_method = self.get_params()
        calc_span = timedelta_to_period(span, series.step())
        
        ema = pdseries.ewm(span=calc_span)
        
        if agg_method == 'mean':
            ema = ema.mean()
        elif agg_method == 'std':
            ema = ema.std()
        elif agg_method == 'var':
            ema = ema.var()
        else:
            raise ValueError('Invalid aggregation method: ' + agg_method)

        ema = ema.dropna()
        debug_info = {
            'alpha': 2/(calc_span+1),
        }
        return (ema, debug_info)

    def get_params(self):
        span = self.get_param('span').value
        agg_method = self.get_param('agg_method').value
        return (span, agg_method)

    def __str__(self):
        return "ExponentialSmoothing(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Exponential smoothing'

    def desc(self):
        return 'Exponential smoothing with decay rate'

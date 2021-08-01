from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean

from ....utils import timedelta_to_period

class ExponentialMovingAverage(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('span', 'Span', 'Span size in time interval (eg: 12h)', '12h'))
        self.add_required_param(String('min_periods', 'Min. periods', 'Min number of periods (eg: 12h). Leave empty for window size.', ''))
        self.add_required_param(Boolean('recursive', 'Recursive', 'Calculate recursively using all past values (vs fixed window size)', True))
        agg_method_options = [
            SelectOption("mean", "Mean"),
            SelectOption("std", "Sample standard dev."),
            SelectOption("var", "Sample variance"),
        ]
        self.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        
        span, min_periods, recursive, agg_method = self.get_params()
        step = series.step()

        calc_span = timedelta_to_period(span, step)

        if min_periods is None:
            calc_min_periods = calc_span
        else:
            calc_min_periods = timedelta_to_period(min_periods, step)
        ema = pdseries.ewm(span=calc_span, adjust=(not recursive), min_periods=calc_min_periods)
        
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
        min_periods = self.get_param('min_periods').value
        recursive = self.get_param('recursive').value
        agg_method = self.get_param('agg_method').value
        return (span, min_periods, recursive, agg_method)

    def __str__(self):
        return "ExponentialMovingAverage(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Exponential moving average'

    def desc(self):
        return 'Exponential moving average with decay rate. Mean, var or std dev.'

from statsmodels.tsa.filters.cf_filter import cffilter

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class CFFilter(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        output_options = [
            SelectOption("trend", "Trend"),
            SelectOption("seasonal", "Seasonality"),
        ]
        self.add_required_param(Select('output', 'Output', 'Output', output_options, output_options[0].code))
        self.add_required_param(String('period_min', 'Period Min', 'Min expected seasonality in periods or time interval (eg: 12h)', '7d'))
        self.add_required_param(String('period_max', 'Period Max', 'Max expected seasonality in periods or time interval (eg: 12h)', '7d'))

    def get_params(self):
        output = self.get_param('output').value
        period_min = self.get_param('period_min').value
        period_max = self.get_param('period_max').value
        return (output, period_min, period_max)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        output, period_min, period_max = self.get_params()
        calc_period_min = timedelta_to_period(period_min, series.step())
        calc_period_max = timedelta_to_period(period_max, series.step())
        cycle, trend = cffilter(pdseries, low=calc_period_min, high=calc_period_max, drift=False)
        result = None
        if output == 'trend':
            result = trend
        elif output == 'seasonal':
            result = cycle
        else:
            raise ValueError('Invalid output: ' + output)
        return (result, {})

    def __str__(self):
        return "CFFilter" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'CFFilter decomposition'

    def desc(self):
        return 'Seasonal-Trend decomposition (LOESS)'

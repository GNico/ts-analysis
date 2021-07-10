import statsmodels.tsa.seasonal as sm

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.string import String
from ....utils import timedelta_to_period

class SeasonalDecompose(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        output_options = [
            SelectOption("trend", "Trend"),
            SelectOption("seasonal", "Seasonality"),
            SelectOption("resid", "Residual"),
        ]
        self.add_required_param(Select('output', 'Output', 'Seasonal decompose output', output_options, output_options[0].code))
        self.add_required_param(String('period', 'Period', 'Expected seasonality in periods or time interval (eg: 12h)', '7d'))
        self.add_required_param(Boolean('two_sided', 'Two sided', 'Calculate moving averages in both directions for robustness', True))

    def get_params(self):
        output = self.get_param('output').value
        period = self.get_param('period').value
        two_sided = self.get_param('two_sided').value
        return (output, period, two_sided)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        output, period, two_sided = self.get_params()
        calc_period = timedelta_to_period(period, series.step())
        model = sm.seasonal_decompose(pdseries, period=calc_period, two_sided=two_sided, model='additive', filt=None, extrapolate_trend=0)
        result = None
        if output == 'resid':
            result = model.resid
        elif output == 'trend':
            result = model.trend
        elif output == 'seasonal':
            result = model.seasonal
        else:
            raise ValueError('Invalid output: ' + output)
        return (result, {})

    def __str__(self):
        return "SeasonalDecompose(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Seasonal decomposition'

    def desc(self):
        return 'Seasonal & trend decomposition using averages'

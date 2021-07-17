import statsmodels.tsa.seasonal as sm

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.string import String
from ....utils import timedelta_to_period

class STL(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        output_options = [
            SelectOption("trend", "Trend"),
            SelectOption("seasonal", "Seasonality"),
            SelectOption("resid", "Residual"),
        ]
        self.add_required_param(Select('output', 'Output', 'STL output', output_options, output_options[0].code))
        self.add_required_param(String('period', 'Period', 'Expected seasonality in periods or time interval (eg: 12h)', '7d'))
        self.add_required_param(String('seasonal_smoother', 'Seasonal smoother', 'Seasonal smoother in periods or time interval (eg: 12h)', '1d'))
        self.add_required_param(Boolean('robust', 'Robust', 'Tolerate larger errors using LOWESS', True))

    def get_params(self):
        output = self.get_param('output').value
        period = self.get_param('period').value
        robust = self.get_param('robust').value
        seasonal_smoother = self.get_param('seasonal_smoother').value
        return (output, period, seasonal_smoother, robust)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        output, period, seasonal_smoother, robust = self.get_params()
        calc_period = timedelta_to_period(period, series.step())
        calc_seasonal_smoother = timedelta_to_period(seasonal_smoother, series.step())
        stl = sm.STL(pdseries, period=calc_period, seasonal=STL.adapt_odd(calc_seasonal_smoother), robust=robust)
        model = stl.fit()
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

    @staticmethod
    def adapt_odd(n):
        # Add 1 if n is odd
        return n + ((n + 1) % 2)

    def __str__(self):
        return "STL" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'STL decomposition'

    def desc(self):
        return 'Seasonal-Trend decomposition (LOESS)'

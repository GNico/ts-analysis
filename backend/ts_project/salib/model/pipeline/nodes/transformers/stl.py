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
        self.add_required_param(Boolean('robust', 'Robust', 'Tolerate larger errors using LOWESS', True))

    def get_params(self):
        output = self.get_param('output').value
        period = self.get_param('period').value
        robust = self.get_param('robust').value
        return (output, period, robust)

    def transform(self, seriess):
        series = seriess[0]
        pdseries = series.pdseries
        output, period, robust = self.get_params()
        calc_period = timedelta_to_period(period, series.step())
        stl = sm.STL(pdseries, seasonal=STL.adapt_period(calc_period), robust=robust)
        result = stl.fit()
        if output == 'resid':
            return result.resid
        elif output == 'trend':
            return result.trend
        elif output == 'seasonal':
            return result.seasonal
        else:
            raise ValueError('Invalid output: ' + output)
        return result

    @staticmethod
    def adapt_period(period):
        # Add 1 if period is odd
        return period + ((period + 1) % 2)

    def __str__(self):
        return "STL(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'STL decomposition'

    def desc(self):
        return 'Seasonal-Trend decomposition (LOESS)'

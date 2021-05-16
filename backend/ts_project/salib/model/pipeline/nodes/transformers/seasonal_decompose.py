import statsmodels.tsa.seasonal as sm

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt

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
        self.add_required_param(BoundedInt('period', 'Period', 'Expected seasonality', 0, None, 24))
        self.add_required_param(Boolean('two_sided', 'Two sided', 'Calculate moving averages in both directions for robustness', True))

    def get_params(self):
        output = self.get_param('output').value
        period = self.get_param('period').value
        two_sided = self.get_param('two_sided').value
        return (output, period, two_sided)

    def transform(self, seriess):
        pdseries = seriess[0].pdseries
        output, period, two_sided = self.get_params()
        result = sm.seasonal_decompose(pdseries, period=period, two_sided=two_sided, model='additive', filt=None, extrapolate_trend=0)
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
        return "SeasonalDecompose(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Seasonal decomposition'

    def desc(self):
        return 'Seasonal & trend decomposition using averages'

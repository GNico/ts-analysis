from statsmodels.tsa.ar_model import AutoReg
import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class AutoRegression(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('lags', '#Lags', 'Lags, in period (eg 12h) or count', '7d'))
        self.add_required_param(String('period', 'Period', 'Seasonality in period (eg 12h) or count. Leave empty for none.', ''))
        output_options = [
            SelectOption("predicted", "Predicted"),
            SelectOption("resid", "Residual"),
        ]
        self.add_required_param(Select('output', 'Output', 'Model output', output_options, output_options[0].code))

    def get_params(self):
        lags = self.get_param('lags').value
        period = self.get_param('period').value
        output = self.get_param('output').value
        return (lags, period, output)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        lags, period, output = self.get_params()

        calc_lags = timedelta_to_period(lags, series.step())
        calc_period = timedelta_to_period(period, series.step()) if period is not None else None
        include_seasonal = calc_period is not None

        ar = AutoReg(pdseries, lags=calc_lags, seasonal=include_seasonal, period=calc_period, old_names=False)
        model = ar.fit()
        
        # Debug info
        if debug:
            debug_info = {
                "summary": str(model.summary())
            }
        else:
            debug_info = {}
        
        result = None
        if output == 'predicted':
            result = model.fittedvalues
        elif output == 'resid':
            result = model.resid
        else:
            raise ValueError('Invalid output: ' + output)

        # print(model.summary())
        return (result, debug_info)

    def __str__(self):
        return "AutoRegression" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Auto-Regression'

    def desc(self):
        return 'Simple SAR model, with lags & seasonality. Fast implementation of SARIMA.'

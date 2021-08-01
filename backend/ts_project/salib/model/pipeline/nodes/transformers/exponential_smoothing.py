import statsmodels.tsa.holtwinters as tsa_hw

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class ExponentialSmoothing(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(Boolean('damped_trend', 'Damped trend', 'Damped trend', True))
        self.add_required_param(String('seasonal_length', 'Seasonal length', 'Season length (in intervals or period, eg. 3h). Leave empty for no seasonality.', '7d'))
        output_options = [
            SelectOption("resid", "Residual"),
            SelectOption("predicted", "Predicted"),
        ]
        self.add_required_param(Select('output', 'Output', 'Model output', output_options, output_options[0].code))


    def get_params(self):
        damped_trend = self.get_param('damped_trend').value
        seasonal_length = self.get_param('seasonal_length').value
        output = self.get_param('output').value
        return (damped_trend, seasonal_length, output)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        damped_trend, seasonal_length, output = self.get_params()
        if seasonal_length is not None and seasonal_length != '':
            calc_seasonal_length = timedelta_to_period(seasonal_length, series.step())
            seasonal = 'add'
        else:
            calc_seasonal_length = None
            seasonal = None

        model = tsa_hw.ExponentialSmoothing(
            pdseries,
            trend='add',
            damped_trend=damped_trend,
            seasonal=seasonal,
            seasonal_periods=calc_seasonal_length,
            initialization_method='estimated',
            use_boxcox=False
        )
        model_fit = model.fit()

        # Debug info
        if debug:
            debug_info = {
                "summary": str(model_fit.summary()),
            }
        else:
            debug_info = {}
       
        result = None
        if output == 'predicted':
            result = model_fit.fittedvalues
        elif output == 'resid':
            result = model_fit.resid
        else:
            raise ValueError('Invalid output: ' + output)

        return (result, debug_info)

    def __str__(self):
        return "ExponentialSmoothing" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Exponential Smoothing'

    def desc(self):
        return 'ExponentialSmoothing model with trend and (optional) seasonality'

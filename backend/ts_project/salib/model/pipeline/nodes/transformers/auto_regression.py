import statsmodels.tsa.arima.model as ar_model
import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.int import BoundedInt
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class AutoRegression(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('p', 'p', 'AR order', '7d'))
        self.add_param(BoundedInt('d', 'd', 'Differencing degree', 0, None, 0))
        self.add_param(String('q', 'q', 'MA order', '0'))

        self.add_param(String('P', 'P', 'Seasonal AR order', '0'))
        self.add_param(BoundedInt('D', 'D', 'Seasonal differencing degree', 0, None, 0))
        self.add_param(String('Q', 'Q', 'Seasonal MA order', '0'))

        self.add_param(String('m', 'm', 'Season length', '0'))

        output_options = [
            SelectOption("predicted", "Predicted"),
            SelectOption("resid", "Residual"),
        ]
        self.add_required_param(Select('output', 'Output', 'Model output', output_options, output_options[0].code))        


    def get_params(self):
        p = self.get_param('p').value
        d = self.get_param('d').value
        q = self.get_param('q').value
        P = self.get_param('P').value
        D = self.get_param('D').value
        Q = self.get_param('Q').value
        m = self.get_param('m').value
        output = self.get_param('output').value
        return (p, d, q, P, D, Q, m, output)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        p, d, q, P, D, Q, m, output = self.get_params()

        order = tuple(map(lambda param: timedelta_to_period(param, series.step()), (p, d, q)))
        seasonal_order = tuple(map(lambda param: timedelta_to_period(param, series.step()), (P, D, Q, m)))

        ar = ar_model.ARIMA(pdseries, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False, trend=None)
        model = ar.fit()
        offset_start = max(sum(order), sum(seasonal_order))
        
        # Debug info
        if debug:
            nlags = min(len(pdseries) // 2 - 1, 40)
            acf_result = stattools.acf(pdseries, nlags=nlags, fft=True)
            pacf_result = stattools.pacf(pdseries, nlags=nlags, method='ols')
            debug_info = {
                "summary": str(model.summary()),
                "offset_start": offset_start,
                "acf": acf_result.tolist(),
                "pacf": pacf_result.tolist()
            }
        else:
            debug_info = {}
        # Drop offset_start elements
        
        result = None
        if output == 'predicted':
            result = model.fittedvalues
        elif output == 'resid':
            result = model.resid
        else:
            raise ValueError('Invalid output: ' + output)

        # print(model.summary())
        return (result[offset_start:], debug_info)

    def __str__(self):
        return "AutoRegression(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Auto-Regression'

    def desc(self):
        return 'SARIMA model, with lags & seasonality. Inputs can be in periods or interval length'

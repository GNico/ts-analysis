import statsmodels.tsa.arima.model as ar_model
import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
from ...params.condition.param_equals_value import ParamEqualsValue
from ...params.int import BoundedInt
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period, lags_range_timedelta_to_period

class SARIMA(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('p', 'p', 'AR order', '7d'))
        self.add_param(BoundedInt('d', 'd', 'Differencing degree', 0, None, 0))
        self.add_param(String('q', 'q', 'MA order', '0'))

        self.add_required_param(Boolean('seasonal', 'Seasonal', 'Seasonal components', False))

        seasonal_p = String('P', 'P', 'Seasonal AR order', '0')
        seasonal_p.add_condition(ParamEqualsValue('seasonal', True))
        self.add_param(seasonal_p)

        seasonal_d = BoundedInt('D', 'D', 'Seasonal differencing degree', 0, None, 0)
        seasonal_d.add_condition(ParamEqualsValue('seasonal', True))
        self.add_param(seasonal_d)
        seasonal_q = String('Q', 'Q', 'Seasonal MA order', '0')
        seasonal_q.add_condition(ParamEqualsValue('seasonal', True))
        self.add_param(seasonal_q)

        seasonal_m = String('m', 'm', 'Season length', '0')
        seasonal_m.add_condition(ParamEqualsValue('seasonal', True))
        self.add_param(seasonal_m)

        output_options = [
            SelectOption("resid", "Residual"),
            SelectOption("predicted", "Predicted"),
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

        calc_p, calc_q = tuple(map(lambda param: lags_range_timedelta_to_period(param, series.step()), (p, q)))
        calc_P, calc_Q = tuple(map(lambda param: lags_range_timedelta_to_period(param, series.step()), (P, Q)))
        calc_m = timedelta_to_period(m, series.step())

        order = (calc_p, d, calc_q)
        seasonal_order = (calc_P, D, calc_Q, calc_m)

        ar = ar_model.ARIMA(pdseries, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False, trend=None)
        model = ar.fit()
        offset_start = max(sum([max(calc_p), d, max(calc_q)]), sum([max(calc_P), D, max(calc_Q)]))

        # Debug info
        if debug:
            debug_info = {
                "summary": str(model.summary()),
                "offset_start": offset_start,
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
        return "SARIMA" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'SARIMA'

    def desc(self):
        return 'SARIMA model, with lags & seasonality. Inputs can be in periods or interval length'

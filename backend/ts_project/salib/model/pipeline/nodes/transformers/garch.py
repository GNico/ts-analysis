from arch import arch_model
import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.int import BoundedInt
from ...params.string import String
from ....utils import timedelta_to_period

class GARCH(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('p', 'p', 'Lag order of errors', '7d'))
        self.add_param(String('q', 'q', 'Lag order of lagged volatility', '0'))

    def get_params(self):
        p = self.get_param('p').value
        q = self.get_param('q').value
        return (p, q)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        p, q = self.get_params()
        calc_p, calc_q = tuple(map(lambda param: timedelta_to_period(param, series.step()), (p, q)))
        ar = arch_model(pdseries, p=calc_p, q=calc_q)
        result = ar.fit()

        # Debug info
        if debug:
            nlags = min(len(pdseries) // 2 - 1, 40)
            acf_result = stattools.acf(pdseries**2, nlags=nlags, fft=True)
            pacf_result = stattools.pacf(pdseries**2, nlags=nlags, method='ols')
            debug_info = {
                "summary": str(result.summary()),
                "acf": acf_result.tolist(),
                "pacf": pacf_result.tolist()}
        else:
            debug_info = {}
        # Drop offset_start elements
        
        return (result.resid, debug_info)

    def __str__(self):
        return "GARCH" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'GARCH'

    def desc(self):
        return 'Generalized ARCH model for volatility modeling. Inputs can be in periods or interval length'

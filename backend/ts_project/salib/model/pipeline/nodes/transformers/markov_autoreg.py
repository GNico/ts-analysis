import statsmodels.api as sm

from ..node_transformer import NodeTransformer
from ...params.int import BoundedInt
from ...params.boolean import Boolean
from ....utils import timedelta_to_period

class MarkovAutoReg(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(BoundedInt('order', 'Order', 'Model order', 0, None, 0))
        self.add_required_param(Boolean('detrend', 'Detrend', 'Detrend', False))

    def get_params(self):
        order = self.get_param('order').value
        detrend = self.get_param('detrend').value
        return (order, detrend)

    def transform(self, seriess):
        series = seriess[0]
        pdseries = series.pdseries
        order, detrend = self.get_params()
        trend = 'ct' if detrend else 'nc'
        model = sm.tsa.MarkovRegression(pdseries, k_regimes=2, order=order, trend=trend)
        result = model.fit()
        return result.smoothed_marginal_probabilities[1]

    def __str__(self):
        return "MarkovAutoReg(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Markov Auto-Regression'

    def desc(self):
        return 'Markov switching Auto-regression'

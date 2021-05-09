import statsmodels.tsa.ar_model as ar_model

from ..node_transformer import NodeTransformer
from ...params.int import BoundedInt

class AutoReg(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(BoundedInt('period', 'Period', 'Expected seasonality', 0, None, 24))
        self.add_required_param(BoundedInt('lags', 'Lags', 'Number of lags to use', 0, None, 6))

    def get_params(self):
        period = self.get_param('period').value
        lags = self.get_param('lags').value
        return (period, lags)

    def transform(self, seriess):
        pdseries = seriess[0].pdseries
        period, lags = self.get_params()
        ar = ar_model.AutoReg(pdseries, seasonal=True, lags=lags, period=period)
        result = ar.fit()
        return result.resid

    def __str__(self):
        return "AutoReg(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Auto-Regression'

    def desc(self):
        return 'Auto-regression with lags & seasonality'

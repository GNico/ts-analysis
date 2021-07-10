import statsmodels.tsa.ar_model as ar_model

from ..node_transformer import NodeTransformer
from ...params.string import String
from ....utils import timedelta_to_period

class AutoRegression(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('lags', 'Lags', 'Number of lags to use or period', '7d'))
        self.add_required_param(String('period', 'Period', 'Expected seasonality in periods or time interval (eg: 12h). Empty or zero to ignore.', '0'))

    def get_params(self):
        period = self.get_param('period').value
        lags = self.get_param('lags').value
        return (period, lags)

    def transform(self, seriess):
        series = seriess[0]
        pdseries = series.pdseries
        period, lags = self.get_params()
        calc_lags = timedelta_to_period(lags, series.step())
        if period == '0' or period == '':
            ar = ar_model.AutoReg(pdseries, lags=calc_lags, seasonal=False, trend='n', old_names=False)
        else:
            calc_period = timedelta_to_period(period, series.step())
            ar = ar_model.AutoReg(pdseries, lags=calc_lags, seasonal=True, period=calc_period, old_names=False)
        result = ar.fit()
        return result.resid

    def __str__(self):
        return "AutoRegression(" + str(self.get_params()) + ")[" + self.id + "]"

    def display(self):
        return 'Auto-Regression'

    def desc(self):
        return 'Auto-regression with lags & seasonality'

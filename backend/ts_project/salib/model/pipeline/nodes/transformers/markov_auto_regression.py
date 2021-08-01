from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression

from ..node_transformer import NodeTransformer
from ...params.string import String
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ....utils import timedelta_to_period

class MarkovAutoRegression(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('lags', '#Lags', 'Lags, in period (eg 12h) or count', '7d'))
        self.add_required_param(BoundedInt('num_regimes', '# Regimes', 'Number of regimes', 2, None, 2))
        self.add_required_param(Boolean('switching_ar', 'Switching AR', 'Switching AR components', False))
        self.add_required_param(Boolean('switching_var', 'Switching var', 'Switching variance components', False))
        self.add_required_param(BoundedInt('output_regime', 'Regime output', 'Output probabilities from specified regime. Value must be [0, num_regimes)', 0, None, 1))

    def get_params(self):
        lags = self.get_param('lags').value
        num_regimes = self.get_param('num_regimes').value
        switching_ar = self.get_param('switching_ar').value
        switching_var = self.get_param('switching_var').value
        output_regime = self.get_param('output_regime').value
        return (lags, num_regimes, switching_ar, switching_var, output_regime)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        lags, num_regimes, switching_ar, switching_var, output_regime = self.get_params()
        calc_lags = timedelta_to_period(lags, series.step())

        model = MarkovAutoregression(pdseries,
            k_regimes=num_regimes,
            trend='nc',
            order=calc_lags,
            switching_ar=switching_ar,
            switching_variance=switching_var
        )
        result = model.fit()
        
        # Debug info
        if debug:
            debug_info = {
                "summary": str(result.summary())
            }
        else:
            debug_info = {}
        
        output = result.smoothed_marginal_probabilities[output_regime]

        # print(model.summary())
        return (output, debug_info)

    def __str__(self):
        return "MarkovAutoRegression" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Markov Auto-Regression'

    def desc(self):
        return 'Markov Auto-Regression with tunable regimes and AR/VAR order switching'

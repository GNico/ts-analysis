import pandas as pd
from scipy import stats

from ..node_transformer import NodeTransformer
from ...params.float import Float

class BoxCox(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_param(Float('lambda', 'Lambda', 'Lambda power, leave empty to estimate.', None))

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        # import pdb;pdb.set_trace()
        debug_info = {
            'lambda': self.lmbda(),
        }
        if self.lmbda() is None:
            transform, fitted_lmbda = stats.boxcox((pdseries+1).tolist(), lmbda=self.lmbda())
            debug_info['fitted_lambda'] = fitted_lmbda
        else:
            transform = stats.boxcox((pdseries+1).tolist(), lmbda=self.lmbda())
            debug_info['fitted_lambda'] = self.lmbda()

        result = pd.Series(transform, index=pdseries.index)
        return (result, debug_info)

    def lmbda(self):
        return self.get_param('lambda').value

    def __str__(self):
        return "BoxCox(" + str(self.lmbda()) + ")[" + self.id + "]"

    def display(self):
        return 'BoxCox'

    def desc(self):
        return 'BoxCox transform with optional lambda'

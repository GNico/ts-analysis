from ..node_transformer import NodeTransformer
from ...params.float import Float

class Rescale(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Float('lower', 'Lower', 'Lower bound', 0.0))
        self.add_required_param(Float('upper', 'Upper', 'Upper bound', 1.0))

    def get_params(self):
        lower = self.get_param('lower').value
        upper = self.get_param('upper').value
        return (lower, upper)

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        lower, upper = self.get_params()

        series_min = pdseries.min()
        series_max = pdseries.max()

        series_std = (pdseries - series_min) / (series_max - series_min)
        series_scaled = series_std * (upper - lower) + lower
        return (series_scaled, {})

    def __str__(self):
        return "Rescale" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Rescale'

    def desc(self):
        return 'Rescale data to given min-max values'

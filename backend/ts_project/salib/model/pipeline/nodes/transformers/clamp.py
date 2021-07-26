from ..node_transformer import NodeTransformer
from ...params.float import Float

class Clamp(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_param(Float('lower', 'Lower', 'Lower bound', 0.0))
        self.add_param(Float('upper', 'Upper', 'Upper bound', 1.0))

    def get_params(self):
        lower = self.get_param('lower').value
        upper = self.get_param('upper').value
        return (lower, upper)

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        lower, upper = self.get_params()
        clamped_series = pdseries.clip(lower=lower, upper=upper)
        return (clamped_series, {})

    def __str__(self):
        return "Clamp" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Clamp'

    def desc(self):
        return 'Assigns values outside boundary to boundary values'

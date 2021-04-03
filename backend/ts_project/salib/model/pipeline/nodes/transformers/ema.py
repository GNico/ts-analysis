from ..node_transformer import NodeTransformer
from ...params.float import BoundedFloat

class EMA(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(BoundedFloat('decay', 'Decay', 'Decay rate', 0, 1, False, 0.9))

    def transform(self, seriess):
        pdseries = seriess[0].pdseries
        min_periods = self.decay()*10
        ema = pdseries.ewm(com=self.decay(), min_periods=min_periods)
        ema = ema.mean().dropna()
        return ema

    def decay(self):
        return self.get_param('decay').value

    def __str__(self):
        return "EMA(" + str(self.decay()) + ")[" + self.id + "]"

    def display(self):
        return 'Exponential moving average'

    def desc(self):
        return 'Exponential moving average with decay rate'

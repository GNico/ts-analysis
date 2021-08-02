from ..node_transformer import NodeTransformer

class AbsValue(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        return (pdseries.abs(), {})

    def __str__(self):
        return "AbsValue[" + self.id + "]"

    def display(self):
        return 'Absolute value'

    def desc(self):
        return 'Take the absolute value for series (modulo)'

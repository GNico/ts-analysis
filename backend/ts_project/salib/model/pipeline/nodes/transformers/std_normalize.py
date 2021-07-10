from ..node_transformer import NodeTransformer

class StdNormalize(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        mean = pdseries.mean()
        std = pdseries.std()
        if std == 0:
            std = 1
        std_series = (pdseries - mean) / std
        return (std_series, {})

    def __str__(self):
        return "Standardize[" + self.id + "]"

    def display(self):
        return 'Standard normalization'

    def desc(self):
        return 'Normalize data such that mean = 0 and std dev = 1'

import scipy

from ..node_transformer import NodeTransformer

class Sigmoid(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        sigmoid = scipy.special.expit(pdseries)
        return (sigmoid, {})

    def __str__(self):
        return "Sigmoid[" + self.id + "]"

    def display(self):
        return 'Sigmoid'

    def desc(self):
        return 'Sigmoid function'

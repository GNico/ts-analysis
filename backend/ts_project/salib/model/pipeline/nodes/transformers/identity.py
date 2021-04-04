from ..node_transformer import NodeTransformer

class Identity(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)

    def transform(self, seriess):
        pdseries = seriess[0].pdseries
        return pdseries

    def __str__(self):
        return "Identity[" + self.id + "]"

    def display(self):
        return 'Identity'

    def desc(self):
        return 'Identity - apply no transformation'

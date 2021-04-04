from ..node_transformer import NodeTransformer

class BinaryMathTransformer(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['left', 'right'])
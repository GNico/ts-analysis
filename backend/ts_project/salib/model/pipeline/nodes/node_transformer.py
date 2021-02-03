from .node import Node
from .node_result import NodeResult
from ...series import Series

class NodeTransformer(Node):

    def __init__(self, id):
        super().__init__(id)

    def execute(self, inputs):
        if len(inputs) != 1:
            raise Exception("NodeTransformer must have exactly 1 input")
        input = inputs[0]
        new_series = Series(self.transform(input.series))
        return NodeResult(self, series=new_series)

    def transform(self, series):
        raise Exception('Unimplemented transform() method for NodeTransformer')
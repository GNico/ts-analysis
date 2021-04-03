import numpy as np

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
        new_pdseries = self.transform_and_validate(input.series)
        new_series = Series(new_pdseries)
        return NodeResult(self, inputs=inputs, series=new_series)

    def transform_and_validate(self, pdseries):
        new_pdseries = self.transform(pdseries)
        new_pdseries.dropna(inplace=True)
        inf_timestamps = list(new_pdseries[np.isinf(new_pdseries)].index)
        if len(inf_timestamps) > 0:
            raise ValueError('Found inf values from %s at: %s' % (self.id, inf_timestamps))
        return new_pdseries

    def transform(self, series):
        raise Exception('Unimplemented transform() method for NodeTransformer')
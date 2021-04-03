import numpy as np
import pandas as pd

from .node import Node
from .node_result import NodeResult
from ...series import Series

class NodeTransformer(Node):

    def __init__(self, id):
        super().__init__(id)
        super().set_required_inputs(1)

    def execute(self, inputs):
        new_pdseries = self.transform_and_validate(inputs)
        new_series = Series(new_pdseries)
        return NodeResult(self, inputs=inputs, series=new_series)

    def transform_and_validate(self, inputs):
        pdseriess = [i.series for i in inputs]
        new_pdseries = self.transform(pdseriess)
        with pd.option_context('mode.use_inf_as_na', True):
            new_pdseries.dropna(inplace=True)
        inf_timestamps = list(new_pdseries[np.isinf(new_pdseries)].index)
        if len(inf_timestamps) > 0:
            raise ValueError('Found inf values from %s at: %s' % (self.id, inf_timestamps))
        return new_pdseries

    def transform(self, seriess):
        raise Exception('Unimplemented transform() method for NodeTransformer')
import numpy as np
import pandas as pd

from .node import Node
from .node_result import NodeResult
from ...series import Series

class NodeTransformer(Node):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['input'])

    def execute(self, inputs):
        new_pdseries = self.transform_and_validate(inputs)
        new_series = Series(new_pdseries)
        return NodeResult(self, inputs=inputs, output_series=new_series)

    def transform_and_validate(self, inputs):
        pdseriess = [i.output_series for i in inputs]
        new_pdseries = self.transform(pdseriess)
        with pd.option_context('mode.use_inf_as_na', True):
            new_pdseries.dropna(inplace=True)
        inf_timestamps = list(new_pdseries[np.isinf(new_pdseries)].index)
        if len(inf_timestamps) > 0:
            raise ValueError('Found inf values from %s at: %s' % (self.id, inf_timestamps))
        return new_pdseries

    def transform(self, seriess):
        raise Exception('Unimplemented transform() method for NodeTransformer')

    @staticmethod
    def rolling_apply_2input(lhs, rhs, func, window_size, center, min_periods):
        result = []
        for i in range(0, len(lhs)):
            lhs_slice = NodeTransformer.window_slice(lhs, i, window_size, center)
            rhs_slice = NodeTransformer.window_slice(rhs, i, window_size, center)
            if len(lhs_slice) < min_periods:
                new_entry = np.nan
            else:
                new_entry = func(lhs_slice, rhs_slice)
            result.append(new_entry)
        return result

    @staticmethod
    def window_slice(data, index, window_size, center):
        start = index - window_size + 1
        end = index + 1
        if center:
            offset = (window_size // 2) - ((window_size-1) % 2)
            start += offset
            end += offset
        clamp_start = max(0, start)
        clamp_end = min(len(data) + 1, end)
        return data[clamp_start:clamp_end]
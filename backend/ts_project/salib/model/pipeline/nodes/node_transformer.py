import numpy as np
import pandas as pd

from .node import Node
from .node_result import NodeResult
from ...series import Series

class NodeTransformer(Node):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['input'])

    def execute(self, inputs, debug):
        new_pdseries, debug_info = self.transform_and_validate(inputs, debug)
        new_series = Series(new_pdseries)
        return NodeResult(self, inputs=inputs, output_series=new_series, debug_info=debug_info)

    def transform_and_validate(self, inputs, debug):
        pdseriess = [i.output_series for i in inputs]
        (new_pdseries, debug_info) = self.transform(pdseriess, debug)
        with pd.option_context('mode.use_inf_as_na', True):
            new_pdseries.dropna(inplace=True)
        inf_timestamps = list(new_pdseries[np.isinf(new_pdseries)].index)
        if len(inf_timestamps) > 0:
            raise ValueError('Found inf values from %s at: %s' % (self.id, inf_timestamps))
        return (new_pdseries, debug_info)

    def transform(self, seriess, debug):
        raise Exception('Unimplemented transform() method for NodeTransformer')

    @staticmethod
    def rolling_dropout(input, func, context_window_size, dropout_window_size, center, min_periods):
        result = []
        for i in range(0, len(input)):
            input_slice = NodeTransformer.window_slice_dropped_out(
                input,
                i,
                context_window_size,
                dropout_window_size,
                center
            )
            if len(input_slice) + dropout_window_size < min_periods:
                new_entry = np.nan
            else:
                new_entry = func(input_slice)
            # print(input, "SLICE #%s" % i, input_slice, new_entry)
            result.append(new_entry)
        return result

    @staticmethod
    def rolling_apply_2input(lhs, rhs, func, window_size, center, min_periods):
        result = []
        rhs_len = len(rhs)
        lhs_len = len(lhs)
        start_offset_lhs = (lhs_len - rhs_len) if lhs_len > rhs_len else 0
        start_offset_rhs = (rhs_len - lhs_len) if rhs_len > lhs_len else 0
        for i in range(0, min(rhs_len, lhs_len)):
            lhs_slice = NodeTransformer.window_slice(lhs, i+start_offset_lhs, window_size, center)
            rhs_slice = NodeTransformer.window_slice(rhs, i+start_offset_rhs, window_size, center)
            if len(lhs_slice) < min_periods:
                new_entry = np.nan
            else:
                new_entry = func(lhs_slice, rhs_slice)
            result.append(new_entry)
        return result

    @staticmethod
    def window_slice(data, index, window_size, center):
        start, end = NodeTransformer.window_slice_idxs(index, window_size, center)
        clamp_start = max(0, start)
        clamp_end = min(len(data), end)
        return data[clamp_start:clamp_end]

    @staticmethod
    def window_slice_dropped_out(data, index, context_window_size, dropout_window_size, center):
        c_start, c_end = NodeTransformer.window_slice_idxs(index, context_window_size, center)
        d_start, d_end = NodeTransformer.window_slice_idxs(index, dropout_window_size, center)
        # print("SLICE #%s" % index, c_start, d_start, d_end, c_end)
        clamp_c_start = max(0, c_start)
        clamp_c_end = min(len(data), c_end)
        clamp_d_start = max(0, d_start-1)
        clamp_d_end = min(len(data), d_end-1)
        # print("SLICE #%s" % index, clamp_c_start, clamp_d_start, clamp_d_end, clamp_c_end)
        return np.concatenate([data[clamp_c_start:clamp_d_start], data[clamp_d_end:clamp_c_end]])

    @staticmethod
    def window_slice_idxs(index, window_size, center):
        start = index - window_size + 1
        end = index + 1
        if center:
            offset = (window_size // 2) - ((window_size-1) % 2)
            start += offset
            end += offset
        return start, end
import pandas as pd

from ..node_transformer import NodeTransformer
from ...params.string import String
from ...params.boolean import Boolean
from ....utils import timedelta_to_period

class Shift(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('delta', 'Time delta', 'Time delta to shift (eg: 1h)', '12h'))
        self.add_required_param(Boolean('shift_values', 'Shift values', 'Shift values or only index', False))

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        delta, shift_values = self.get_params()
        calc_shift = timedelta_to_period(delta, series.step(), validate=False)
        freq = series.interval if shift_values else None
        s_shifted = pdseries.shift(calc_shift, freq=freq)
        return (s_shifted, {})

    def get_params(self):
        delta = self.get_param('delta').value
        shift_values = self.get_param('shift_values').value
        return (delta, shift_values)

    def __str__(self):
        return "Shift" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Time shift'

    def desc(self):
        return 'Shift series in time by a fixed time delta'

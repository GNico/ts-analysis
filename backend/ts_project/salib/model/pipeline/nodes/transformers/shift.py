import pandas as pd

from ..node_transformer import NodeTransformer
from ...params.string import String

class Shift(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('delta', 'Time delta', 'Time delta to shift (eg: 1h)', '12h'))


    def transform(self, series):
        pdseries = series.pdseries
        s_shifted = pd.Series(pdseries.values, pdseries.index + pd.Timedelta(self.delta()))
        s_shifted = s_shifted.append(
            pd.Series(index=pdseries.index, dtype="float64")
        )
        s_shifted = s_shifted.iloc[
            s_shifted.index.duplicated() == False
        ]
        s_shifted = s_shifted.sort_index()
        s_shifted.name = pdseries.name
        return s_shifted

    def delta(self):
        return self.get_param('delta').value

    def __str__(self):
        return "Shift(" + str(self.delta()) + ")[" + self.id + "]"

    def display(self):
        return 'Time shift'

    def desc(self):
        return 'Shift series in time by a fixed time delta'

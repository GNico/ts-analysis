from ..node_transformer import NodeTransformer
from .rolling_aggregate_common import RollingAggregateCommon

class RollingAggregateMean(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        RollingAggregateCommon.add_common_params(self)

    def transform(self, series):
        pdseries = series.pdseries
        window, center, min_periods = RollingAggregateCommon.get_common_params(self)
        return pdseries.rolling(window=window, center=center, min_periods=min_periods).agg('mean')

    def __str__(self):
        return "RollingAggregateMean(" + RollingAggregateCommon.str_params(self) + ")[" + self.id + "]"

    def display(self):
        return 'Rolling Aggregate Mean'

    def desc(self):
        return 'Rolling aggregate using mean'
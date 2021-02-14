from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt


class RollingAggregate(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_common_params()

    def transform(self, series):
        pdseries = series.pdseries
        window, center, min_periods, agg_method = self.get_common_params()
        return pdseries.rolling(window=window, center=center, min_periods=min_periods).agg(agg_method)

    def add_common_params(node):
        node.add_required_param(String('window', 'Window', 'Window size in time interval (eg: 1h)', '30m'))
        node.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        node.add_required_param(BoundedInt('min_periods', 'Min. periods', 'Min number of periods', 0, None))
        agg_method_options = [
            SelectOption("mean", "Mean"),
            SelectOption("median", "Median"),
            SelectOption("sum", "Sum"),
            SelectOption("min", "Min"),
            SelectOption("max", "Max"),
            SelectOption("quantile", "Quantile"),
            SelectOption("iqr", "Inter-quartile range"),
            SelectOption("idr", "Inter-decile range"),
            SelectOption("count", "Value count"),
            SelectOption("nnz", "Non zero count"),
            SelectOption("nunique", "Unique count"),
            SelectOption("std", "Sample standard dev."),
            SelectOption("var", "Sample variance"),
            SelectOption("skew", "Sample skewness"),
            SelectOption("kurt", "Sample kurtosis")
        ]
        node.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))        

    def get_common_params(node):
        window = node.get_param('window').value
        center = node.get_param('center').value
        min_periods = node.get_param('min_periods').value
        agg_method = node.get_param('agg_method').value
        return (window, center, min_periods, agg_method)

    def str_common_params(node):
        return ','.join(map(lambda p: str(p), RollingAggregateCommon.get_common_params(node)))

    def __str__(self):
        return "RollingAggregate(" + self.str_common_params(self) + ")[" + self.id + "]"

    def display(self):
        return 'Rolling Aggregate'

    def desc(self):
        return 'Rolling aggregate'
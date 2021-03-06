from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ...params.float import BoundedFloat
from ...params.condition.param_equals_value import ParamEqualsValue

class RollingAggregate(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_common_params()
        quantile_range = BoundedFloat('quantile_range', 'Quantile range', 'Quantile range [q;1-q]', 0, 0.5, False, 0.25)
        quantile_range.add_condition(ParamEqualsValue('agg_method', 'quantile'))
        self.add_param(quantile_range)
        self._closed = None

    def add_common_params(self):
        self.add_required_param(String('window', 'Window', 'Window size in time interval (eg: 1h)', '30m'))
        self.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        self.add_required_param(BoundedInt('min_periods', 'Min. periods', 'Min number of periods', 0, None, 0))
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
        self.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))        

    def get_common_params(self):
        window = self.get_param('window').value
        center = self.get_param('center').value
        min_periods = self.get_param('min_periods').value
        agg_method = self.get_param('agg_method').value
        return (window, center, min_periods, agg_method)

    def str_common_params(self):
        return ','.join(map(lambda p: str(p), RollingAggregateCommon.get_common_params(self)))

    def __str__(self):
        return "RollingAggregate(" + self.str_common_params(self) + ")[" + self.id + "]"

    def display(self):
        return 'Rolling Aggregate'

    def desc(self):
        return 'Rolling aggregate'

    def transform(self, series):
        return self.transform_pdseries(series.pdseries)

    def transform_pdseries(self, s):
        window, center, min_periods, agg = self.get_common_params()

        rolling = s.rolling(
            window=window,
            center=center,
            min_periods=min_periods,
            closed=self._closed,
        )

        if agg in [
            'mean',
            'median',
            'sum',
            'min',
            'max',
            'count',
            'std',
            'var',
            'skew',
            'kurt',
        ]:
            s_rolling = rolling.agg(agg)
        elif agg == 'nunique':
            s_rolling = rolling.agg(lambda x: len(np.unique(x.dropna())))
        elif agg == 'nnz':
            s_rolling = rolling.agg(np.count_nonzero)
        elif agg == 'iqr':
            s_rolling = rolling.quantile(0.75) - rolling.quantile(0.25)
        elif agg == 'idr':
            s_rolling = rolling.quantile(0.9) - rolling.quantile(0.1)
        elif agg == 'quantile':
            quantile_range = self.get_param('quantile_range').value
            s_rolling = rolling.quantile(1.0 - quantile_range) - rolling.quantile(quantile_range)
        else:
            raise ValueError('Invalid aggregation method: ' + agg)

        s_rolling.name = s.name
        return s_rolling
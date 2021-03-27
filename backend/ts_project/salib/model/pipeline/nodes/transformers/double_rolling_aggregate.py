from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ...params.float import BoundedFloat
from ...params.condition.param_equals_value import ParamEqualsValue

from .rolling_aggregate import RollingAggregate

class DoubleRollingAggregate(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_common_params()
        quantile_range_lhs = BoundedFloat('quantile_range_lhs', 'Quantile range', 'Quantile range [q;1-q]', 0, 0.5, False, 0.25)
        quantile_range_lhs.add_condition(ParamEqualsValue('agg_method_lhs', 'quantile'))
        self.add_param(quantile_range_lhs)
        quantile_range_rhs = BoundedFloat('quantile_range_rhs', 'Quantile range', 'Quantile range [q;1-q]', 0, 0.5, False, 0.25)
        quantile_range_rhs.add_condition(ParamEqualsValue('agg_method_rhs', 'quantile'))
        self.add_param(quantile_range_rhs)

    def add_common_params(self):
        self.add_required_param(String('window_lhs', 'Left window', 'Left window size in time interval (eg: 1h)', '12h'))
        self.add_required_param(String('window_rhs', 'Left window', 'Left window size in time interval (eg: 1h)', '6h'))
        self.add_required_param(Boolean('center', 'Center', 'Center aggregation windows', False))
        self.add_required_param(BoundedInt('min_periods_lhs', 'Left window min. periods', 'Min number of periods for left window', 0, None, 0))
        self.add_required_param(BoundedInt('min_periods_rhs', 'Right window min. periods', 'Min number of periods for right window', 0, None, 0))
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
        self.add_required_param(Select('agg_method_lhs', 'Left aggregation', 'Aggregation method for left window', agg_method_options, agg_method_options[0].code))        
        self.add_required_param(Select('agg_method_rhs', 'Right aggregation', 'Aggregation method for right window', agg_method_options, agg_method_options[0].code))        
        diff_method_options = [
            SelectOption("diff", "Difference"),
            SelectOption("l1", "L1 distance metric (mod sum)"),
            SelectOption("rel_diff", "Relative difference"),
            SelectOption("abs_rel_diff", "Absolute relative difference"),
        ]
        self.add_required_param(Select('diff', 'Difference metric', 'Difference metric between window values', diff_method_options, diff_method_options[0].code))        

    def get_common_params(self):
        window_lhs = self.get_param('window_lhs').value
        window_rhs = self.get_param('window_rhs').value
        center = self.get_param('center').value
        min_periods_lhs = self.get_param('min_periods_lhs').value
        min_periods_rhs = self.get_param('min_periods_rhs').value
        agg_method_lhs = self.get_param('agg_method_lhs').value
        agg_method_rhs = self.get_param('agg_method_rhs').value
        diff = self.get_param('diff').value
        return (window_lhs, window_rhs, center, min_periods_lhs, min_periods_rhs, agg_method_lhs, agg_method_rhs, diff)

    def str_common_params(self):
        return ','.join(map(lambda p: str(p), DoubleRollingAggregateCommon.get_common_params(self)))

    def __str__(self):
        return "DoubleRollingAggregate(" + self.str_common_params(self) + ")[" + self.id + "]"

    def display(self):
        return 'Double Rolling Aggregate'

    def desc(self):
        return 'Double rolling aggregate'

    def transform(self, series):
        s = series.pdseries
        window_lhs, window_rhs, center, min_periods_lhs, min_periods_rhs, agg_method_lhs, agg_method_rhs, diff = self.get_common_params()

        if center:
            ra_left = RollingAggregate('interal_left')
            ra_left.set_param_value('agg_method', agg_method_lhs)
            ra_left.set_param_value('window', window_lhs)
            ra_left.set_param_value('min_periods', min_periods_lhs)
            ra_left.set_param_value('center', False)
            ra_left.set_param_value('quantile_range', self.get_param('quantile_range_lhs').value)
            ra_left._closed = "left"
            s_rolling_left = ra_left.transform_pdseries(s)

            s_reversed = pd.Series(
                s.values[::-1],
                index=pd.DatetimeIndex(
                    [
                        s.index[0] + (s.index[-1] - s.index[i])
                        for i in range(len(s) - 1, -1, -1)
                    ]
                ),
            )

            ra_right = RollingAggregate('interal_right')
            ra_right.set_param_value('agg_method', agg_method_rhs)
            ra_right.set_param_value('window', window_rhs)
            ra_right.set_param_value('min_periods', min_periods_rhs)
            ra_right.set_param_value('center', False)
            ra_right.set_param_value('quantile_range', self.get_param('quantile_range_rhs').value)
            s_rolling_right = pd.Series(
                ra_right.transform_pdseries(s_reversed)
                .iloc[::-1]
                .values,
                index=s.index,
            )
            s_rolling_right.name = s.name
        else:
            s_shifted = pd.Series(s.values, s.index + pd.Timedelta(window[1]))
            s_shifted = s_shifted.append(
                pd.Series(index=s.index, dtype="float64")
            )
            s_shifted = s_shifted.iloc[
                s_shifted.index.duplicated() == False
            ]
            s_shifted = s_shifted.sort_index()
            s_shifted.name = s.name

            ra_left = RollingAggregate('interal_left')
            ra_left.set_param_value('agg_method', agg_method_lhs)
            ra_left.set_param_value('window', window_lhs)
            ra_left.set_param_value('min_periods', min_periods_lhs)
            ra_left.set_param_value('center', False)
            ra_left.set_param_value('quantile_range', self.get_param('quantile_range_lhs').value)
            s_rolling_left = ra_left.transform_pdseries(s_shifted)
            s_rolling_left = s_rolling_left[s.index]

            ra_right = RollingAggregate('interal_right')
            ra_right.set_param_value('agg_method', agg_method_rhs)
            ra_right.set_param_value('window', window_rhs)
            ra_right.set_param_value('min_periods', min_periods_rhs)
            ra_right.set_param_value('center', False)
            ra_right.set_param_value('quantile_range', self.get_param('quantile_range_rhs').value)
            s_rolling_right = ra_right.transform_pdseries(s)

        if diff == "diff":
            return s_rolling_right - s_rolling_left
        if diff == "l1":
            return abs(s_rolling_right - s_rolling_left)
        if diff == "rel_diff":
            return (s_rolling_right - s_rolling_left) / s_rolling_left
        if diff == "abs_rel_diff":
            return abs(s_rolling_right - s_rolling_left) / s_rolling_left

        raise ValueError("Invalid value of diff")
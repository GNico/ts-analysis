from scipy import stats
import pandas as pd
import numpy as np

from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ....utils import timedelta_to_period

class MultiRollingAggregate(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['lhs', 'rhs'])
        self.add_common_params()

    def add_common_params(self):
        self.add_required_param(String('window', 'Window', 'Window size in time interval (eg: 12h)', '12h'))
        self.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        self.add_required_param(String('min_periods', 'Min. periods', 'Min number of periods (eg: 12h). Leave empty for window size.', ''))
        agg_method_options = [
            SelectOption("proportion", "Proportion"),
            SelectOption("ks", "Kolmorogov-Smirnov"),
            SelectOption("correlation_pearson", "Pearson Correlation"),
            SelectOption("correlation_kendall", "Kendall Correlation"),
            SelectOption("correlation_spearman", "Spearman Correlation"),
        ]
        self.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))        

    def get_common_params(self):
        window = self.get_param('window').value
        center = self.get_param('center').value
        min_periods = self.get_param('min_periods').value
        agg_method = self.get_param('agg_method').value
        return (window, center, min_periods, agg_method)

    def str_common_params(self):
        return ','.join(map(lambda p: str(p), self.get_common_params()))

    def __str__(self):
        return "MultiRollingAggregate(" + self.str_common_params() + ")[" + self.id + "]"

    def display(self):
        return 'Multi Rolling Aggregate'

    def desc(self):
        return 'Multi Rolling aggregate'

    def transform(self, seriess, debug):
        lhs, rhs = seriess[0], seriess[1]
        NodeTransformer.validate_input_steps_spans(lhs, rhs)
        transformed_values = self.transform_values(lhs, rhs)
        new_index = lhs.pdseries.index if lhs.span() < rhs.span() else rhs.pdseries.index
        return (pd.Series(transformed_values, index=new_index), {})

    def transform_values(self, lhs, rhs):
        window_str, center, min_periods, agg = self.get_common_params()

        window = timedelta_to_period(window_str, lhs.step())

        if min_periods is None:
            calc_min_periods = window
        else:
            calc_min_periods = timedelta_to_period(min_periods, lhs.step())

        if agg == 'proportion':
            rolling_func = MultiRollingAggregate.func_proportion
        elif agg == 'ks':
            rolling_func = MultiRollingAggregate.func_ks_2samp
        elif agg == 'correlation_pearson':
            rolling_func = MultiRollingAggregate.func_correlation_pearson
        elif agg == 'correlation_kendall':
            rolling_func = MultiRollingAggregate.func_correlation_kendall
        elif agg == 'correlation_spearman':
            rolling_func = MultiRollingAggregate.func_correlation_spearman
        else:
            raise ValueError('Invalid aggregation method: ' + agg)

        return NodeTransformer.rolling_apply_2input(
                    lhs.pdseries.values,
                    rhs.pdseries.values,
                    rolling_func,
                    window,
                    center,
                    calc_min_periods
                )

    @staticmethod
    def func_ks_2samp(lhs, rhs):
        return stats.ks_2samp(lhs, rhs)[1]

    @staticmethod
    def func_proportion(lhs, rhs):
        rhs_sum = sum(rhs)
        if rhs_sum == 0:
            return 0.0
        else:
            return sum(lhs) / rhs_sum

    @staticmethod
    def func_correlation(lhs, rhs, corr_func):
        if len(lhs) > 1 and len(rhs) > 1:
            value, _ = corr_func(lhs, rhs)
            if not np.isfinite(value):
                value = 0.0
        else:
            value = np.nan
        return value

    @staticmethod
    def func_correlation_pearson(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, stats.pearsonr)

    @staticmethod
    def func_correlation_kendall(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, lambda x,y: stats.weightedtau(x, y, rank=False))

    @staticmethod
    def func_correlation_spearman(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, stats.spearmanr)

import pandas as pd
import numpy as np

from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ....utils import timedelta_to_period

class MultiRollingAggregate(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        super().set_input_names(['lhs', 'rhs'])
        self.add_common_params()

    def add_common_params(self):
        self.add_required_param(String('window', 'Window', 'Window size in time interval (eg: 12h)', '12h'))
        self.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        self.add_required_param(BoundedInt('min_periods', 'Min. periods', 'Min number of periods', 0, None, 0))
        agg_method_options = [
            SelectOption("correlation_pearson", "Pearson Correlation"),
            SelectOption("correlation_kendall", "Kendall Correlation"),
            SelectOption("correlation_spearman", "Spearman Correlation"),
            SelectOption("proportion", "Proportion"),
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
        MultiRollingAggregate.validate_input_steps_spans(lhs, rhs)
        transformed_values = self.transform_values(lhs, rhs)
        return (pd.Series(transformed_values, index=lhs.pdseries.index), {})

    def transform_values(self, lhs, rhs):
        window_str, center, min_periods, agg = self.get_common_params()
        window = timedelta_to_period(window_str, lhs.step())

        if agg == 'proportion':
            rolling_func = MultiRollingAggregate.func_proportion
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
                    min_periods
                )

    @staticmethod
    def func_proportion(lhs, rhs):
        rhs_sum = sum(rhs)
        if rhs_sum == 0:
            return np.nan
        else:
            return sum(lhs) / rhs_sum

    @staticmethod
    def func_correlation(lhs, rhs, method):
        lhs = pd.Series(lhs)
        rhs = pd.Series(rhs)
        if len(lhs) > 1 and len(rhs) > 1:
            return lhs.corr(rhs, method=method)
        else:
            return np.nan

    @staticmethod
    def func_correlation_pearson(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, 'pearson')

    @staticmethod
    def func_correlation_kendall(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, 'kendall')

    @staticmethod
    def func_correlation_spearman(lhs, rhs):
        return MultiRollingAggregate.func_correlation(lhs, rhs, 'spearman')

    @staticmethod
    def validate_input_steps_spans(lhs, rhs):
        if lhs.step() != rhs.step():
            err_vars = (lhs.step(), rhs.step())
            raise ValueError('Inputs must have same step interval: lhs: %s != rhs: %s' % err_vars)
        if lhs.span() != rhs.span():
            err_vars = (lhs.start, lhs.end, rhs.start, rhs.end)
            raise ValueError('Inputs must have same span: lhs: %s-%s != rhs: %s-%s' % err_vars)
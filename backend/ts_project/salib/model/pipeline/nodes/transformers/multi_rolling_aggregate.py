import pandas as pd
import numpy as np

from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.int import BoundedInt

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
        return "MultiRollingAggregate(" + self.str_common_params(self) + ")[" + self.id + "]"

    def display(self):
        return 'Multi Rolling Aggregate'

    def desc(self):
        return 'Multi Rolling aggregate'

    def transform(self, seriess):
        df = pd.DataFrame({
            self.input_names[0]: seriess[0].pdseries,
            self.input_names[1]: seriess[1].pdseries
        })
        return self.transform_df(df)

    def transform_df(self, df):
        window, center, min_periods, agg = self.get_common_params()

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

        rolling = df.rolling(
            window=window,
            center=center,
            min_periods=min_periods
        )

        rolling = rolling.apply(rolling_func, kwargs={'df':df}, raw=False)['lhs']
        return rolling

    @staticmethod
    def func_proportion(window, df):
        lhs = df.loc[window.index, 'lhs']
        rhs = df.loc[window.index, 'rhs']
        return lhs.sum() / rhs.sum()

    @staticmethod
    def func_correlation(window, df, method):
        lhs = df.loc[window.index, 'lhs']
        rhs = df.loc[window.index, 'rhs']
        if len(lhs) > 1 and len(rhs) > 1:
            return lhs.corr(rhs, method=method)
        else:
            return np.nan

    @staticmethod
    def func_correlation_pearson(window, df):
        return MultiRollingAggregate.func_correlation(window, df, 'pearson')

    @staticmethod
    def func_correlation_kendall(window, df):
        return MultiRollingAggregate.func_correlation(window, df, 'kendall')

    @staticmethod
    def func_correlation_spearman(window, df):
        return MultiRollingAggregate.func_correlation(window, df, 'spearman')
import numpy as np
import pandas as pd

from ..node_transformer import NodeTransformer

from ...params.string import String
from ...params.select import Select, SelectOption
from ...params.boolean import Boolean
from ...params.float import BoundedFloat
from ...params.condition.param_equals_value import ParamEqualsValue
from ....utils import timedelta_to_period

class Dropout(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_common_params()

    def add_common_params(self):
        self.add_required_param(String('dropout_window', 'Dropout window', 'Window size in time interval (eg: 12h). Must be smaller than the context window.', '12h'))
        self.add_required_param(String('context_window', 'Context window', 'Window size in time interval (eg: 12h). Must be larger than the dropout window.', '7d'))
        self.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        self.add_required_param(String('min_periods', 'Min. periods', 'Min number of periods (eg: 12h). Leave empty for window size.', ''))
        agg_method_options = [
            SelectOption("mean", "Mean"),
            SelectOption("median", "Median"),
            SelectOption("sum", "Sum"),
            SelectOption("min", "Min"),
            SelectOption("max", "Max"),
            SelectOption("count", "Value count"),
            SelectOption("nnz", "Non zero count"),
            SelectOption("nunique", "Unique count"),
            SelectOption("std", "Sample standard dev."),
            SelectOption("var", "Sample variance"),
            SelectOption("skew", "Sample skewness"),
            SelectOption("kurt", "Sample kurtosis")
        ]
        self.add_required_param(Select('agg_method', 'Aggregation', 'Aggregation method', agg_method_options, agg_method_options[0].code))

        combine_method_options = [
            SelectOption("sub", "Substract"),
            SelectOption("prop", "Ratio"),
        ]
        self.add_required_param(Select('combine_method', 'Combine func.', 'Combination method for context-dropout windows', combine_method_options, combine_method_options[0].code))

        combine_method_order_options = [
            SelectOption("context-dropout", "Context,dropout"),
            SelectOption("dropout-context", "Dropout,context"),
        ]
        self.add_required_param(Select('combine_method_order', 'Combine order', 'Combination method parameters order', combine_method_order_options, combine_method_order_options[0].code))

    def get_params(self):
        context_window = self.get_param('context_window').value
        dropout_window = self.get_param('dropout_window').value
        agg_method = self.get_param('agg_method').value
        center = self.get_param('center').value
        min_periods = self.get_param('min_periods').value
        combine_method = self.get_param('combine_method').value
        combine_method_order = self.get_param('combine_method_order').value
        return (context_window, dropout_window, agg_method, center, min_periods, combine_method, combine_method_order)

    def __str__(self):
        return "Dropout" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Dropout'

    def desc(self):
        return 'Dropout window analysis'

    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        step = seriess[0].step()

        context_window, dropout_window, agg, center, min_periods, combine_method, combine_method_order = self.get_params()
        calc_context_window = timedelta_to_period(context_window, step)
        calc_dropout_window = timedelta_to_period(dropout_window, step)
        if calc_dropout_window >= calc_context_window:
            raise ValueError('Dropout window must be smaller than context window')

        if min_periods is None or min_periods == '':
            calc_min_periods = calc_context_window
        else:
            calc_min_periods = timedelta_to_period(min_periods, step)

        agg_func = None
        if agg == 'mean':
            agg_func = np.mean
        elif agg == 'median':
            agg_func = np.median
        elif agg == 'sum':
            agg_func = np.sum
        elif agg == 'min':
            agg_func = np.min
        elif agg == 'max':
            agg_func = np.max
        elif agg == 'std':
            agg_func = np.std,
        elif agg == 'var':
            agg_func = np.var
        elif agg == 'nunique':
            agg_func = lambda x: len(np.unique(x.dropna()))
        elif agg == 'nnz':
            agg_func = np.count_nonzero
        else:
            raise ValueError('Invalid aggregation method: ' + agg)

        combine_func = None
        if combine_method == 'sub':
            combine_func = np.subtract
        elif combine_method == 'prop':
            combine_func = np.divide
        else:
            raise ValueError('Invalid combination method: ' + combine_method)

        context_first = (combine_method_order == "context-dropout")

        transformed_values = NodeTransformer.rolling_dropout(pdseries.values, agg_func, combine_func, context_first, calc_context_window, calc_dropout_window, center=center, min_periods=calc_min_periods)
        result = pd.Series(transformed_values, index=pdseries.index)
        return (result, {})

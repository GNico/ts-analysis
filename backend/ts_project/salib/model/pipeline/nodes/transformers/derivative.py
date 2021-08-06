import pandas as pd

from ..node_transformer import NodeTransformer
from ...params.string import String
from ...params.select import Select, SelectOption
from ....utils import timedelta_to_period

class Derivative(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('lag', 'Lag', 'Lag to apply (eg: 1h, 10)', '12h'))
        operators = [
            SelectOption('sub', 'Substract'),
            SelectOption('l1', 'L1 distance metric (mod sub)'),
            SelectOption('rel_diff', 'Relative difference'),
            SelectOption('abs_rel_diff', 'Absolute relative difference'),
        ]
        self.add_required_param(Select('metric', 'Difference metric', 'Difference metric between window values', operators, operators[0].code))

    def get_params(self):
        lag = self.get_param('lag').value
        metric = self.get_param('metric').value
        return (lag, metric)

    def __str__(self):
        return "Derivative" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'Derivative'

    def desc(self):
        return 'Derivative operator'

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        lag, metric = self.get_params()
        calc_lag = timedelta_to_period(lag, series.step(), validate=False)
        lhs = pdseries
        rhs = pdseries.shift(calc_lag)

        result = None
        if metric == 'sub':
            result = lhs - rhs
        if metric == 'l1':
            result = abs(lhs - rhs)
        if metric == 'rel_diff':
            result = (lhs - rhs) / rhs
        if metric == 'abs_rel_diff':
            result = abs(lhs - rhs) / rhs

        if result is not None:
            return (result.dropna(), {})
        else:
            raise ValueError('Invalid metric option')
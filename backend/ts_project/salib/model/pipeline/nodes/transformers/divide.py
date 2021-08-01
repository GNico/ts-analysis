import numpy as np

from .binary_math_transformer import BinaryMathTransformer
from ...params.select import Select, SelectOption
from ...params.int import Int

class Divide(BinaryMathTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_param(Int('zero_div', 'Zero div:', 'Value for division by zero. Empty to skip', 0))

    def __str__(self):
        return 'Divide(' + str(self.get_zero_div()) + ')[' + self.id + ']'

    def display(self):
        return 'Divide'

    def desc(self):
        return 'Divide operator'

    def get_zero_div(self):
        return self.get_param('zero_div').value

    def transform(self, seriess, debug):
        lhs = seriess[0].pdseries
        rhs = seriess[1].pdseries
        zero_div_replacement = np.nan if self.get_zero_div() is None else self.get_zero_div()
        result = (lhs / rhs).replace([np.inf,-np.inf], zero_div_replacement).dropna()
        return (result, {})

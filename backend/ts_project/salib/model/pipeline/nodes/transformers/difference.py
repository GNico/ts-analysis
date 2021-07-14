from .binary_math_transformer import BinaryMathTransformer
from ...params.select import Select, SelectOption

class Difference(BinaryMathTransformer):

    def __init__(self, id):
        super().__init__(id)
        operators = [
            SelectOption('sub', 'Substract'),
            SelectOption('l1', 'L1 distance metric (mod sum)'),
            SelectOption('rel_diff', 'Relative difference'),
            SelectOption('abs_rel_diff', 'Absolute relative difference'),
        ]
        self.add_required_param(Select('metric', 'Difference metric', 'Difference metric between window values', operators, operators[0].code))

    def __str__(self):
        return 'Difference(' + ','.join(map(str, self.sources)) + ')[' + self.id + ']'

    def display(self):
        return 'Difference'

    def desc(self):
        return 'Difference operator'

    def transform(self, seriess, debug):
        lhs = seriess[0].pdseries
        rhs = seriess[1].pdseries

        metric = self.get_param('metric').value

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
            return (result, {})
        else:
            raise ValueError('Invalid metric option')
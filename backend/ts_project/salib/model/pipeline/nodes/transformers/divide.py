from .binary_math_transformer import BinaryMathTransformer
from ...params.select import Select, SelectOption

class Divide(BinaryMathTransformer):

    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return 'Divide(' + ','.join(map(str, self.sources)) + ')[' + self.id + ']'

    def display(self):
        return 'Divide'

    def desc(self):
        return 'Divide operator'

    def transform(self, seriess, debug):
        lhs = seriess[0].pdseries
        rhs = seriess[1].pdseries
        result = lhs / rhs
        return (result, {})

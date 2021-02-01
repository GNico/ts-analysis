from ._or import Or

class Root(Or):

    def __init__(self):
        super().__init__('_Root')

    def __str__(self):
        return '_Root(' + ','.join([s.id for s in self.sources]) + ')'

    def desc(self):
        return 'Root node'

    def display(self):
        return '_Root'

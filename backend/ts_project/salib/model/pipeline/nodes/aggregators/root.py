from .union import Union

class Root(Union):

    def __init__(self):
        super().__init__('_Root')

    def __str__(self):
        return '_Root(' + ','.join(map(str,self.sources)) + ')'

    def desc(self):
        return 'Root node'

    def display(self):
        return '_Root'

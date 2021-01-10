from .param import Param

class Float(Param):

    def __init__(self, id, value=None):
        self.klass = 'Float'
        self.id = id
        self.value = value

class BoundedFloat(Param):

    def __init__(self, id, min, max, value=None):
        self.klass = 'BoundedFloat'
        self.id = id
        self.min = min
        self.max = max
        self.value = value

    def validate(self):
        if self.value < self.min or self.value > self.max:
            raise Exception('Invalid range for bounded float, ' + self.value + 
                            ' is not within range [' + self.min + ', ' + self.max +']')

    def definition(self):
        output = super().definition()
        output['min'] = self.min
        output['max'] = self.max
        return output
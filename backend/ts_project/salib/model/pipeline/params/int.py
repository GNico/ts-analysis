from .param import Param

class Int(Param):

    def __init__(self, id, display, desc, value=None):
        super().__init__(id, 'Int', display, desc, value)

class BoundedInt(Param):

    def __init__(self, id, display, desc, min, max, value=None):
        super().__init__(id, 'BoundedInt', display, desc, value)
        self.min = min
        self.max = max

    def validate(self):
        super().validate()
        if (self.min is not None and self.value < self.min) or (self.max is not None and self.value > self.max):
            raise Exception('Invalid range for bounded int, ' + self.value + 
                            ' is not within range [' + self.min + ', ' + self.max +']')

    def definition(self):
        output = super().definition()
        output['min'] = self.min
        output['max'] = self.max
        return output
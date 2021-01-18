from .param import Param

class Float(Param):

    def __init__(self, id, display, desc, value=None):
        super().__init__(id, 'Float', display, desc, value)

class BoundedFloat(Param):

    def __init__(self, id, display, desc, min, max, value=None):
        super().__init__(id, 'BoundedFloat', display, desc, value)
        self.min = min
        self.max = max

    def validate(self):
        if self.value < self.min or self.value > self.max:
            raise Exception('Invalid range for bounded float, ' + self.value + 
                            ' is not within range [' + self.min + ', ' + self.max +']')

    def definition(self):
        output = super().definition()
        output['min'] = self.min
        output['max'] = self.max
        return output
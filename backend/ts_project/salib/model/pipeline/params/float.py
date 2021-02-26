from .param import Param

class Float(Param):

    def __init__(self, id, display, desc, value=None):
        super().__init__(id, 'Float', display, desc, value)

class BoundedFloat(Param):

    def __init__(self, id, display, desc, min, max, strict, value=None):
        super().__init__(id, 'BoundedFloat', display, desc, value)
        self.min = min
        self.max = max
        if not isinstance(strict, tuple):
            strict = (strict,strict)
        self.strict_min, self.strict_max = strict

    def validate(self):
        if self.min is not None:
            if self.strict_min:
                if self.value <= self.min:
                    self.raise_exception()
            else:
                if self.value < self.min:
                    self.raise_exception()
        if self.max is not None:
            if self.strict_max:
                if self.value >= self.max:
                    self.raise_exception()
            else:
                if self.value > self.max:
                    self.raise_exception()



    def raise_exception(self):
        lower_bound = '(' if self.strict_min else '['
        upper_bound = ')' if self.strict_max else ']'
        raise Exception("Invalid range for bounded float: %s is not within range %s%s,%s%s" % (self.value, lower_bound, self.min, self.max, upper_bound))

    def definition(self):
        output = super().definition()
        output['min'] = self.min
        output['max'] = self.max
        output['strict_min'] = self.strict_min
        output['strict_max'] = self.strict_max
        return output
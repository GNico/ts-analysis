from .param import Param

class Select(Param):

    def __init__(self, id, display, desc, options, value=None):
        super().__init__(id, 'Select', display, desc, value)
        self.options = options

    def validate(self):
        option_codes = [option.code for option in self.options]
        if self.value not in option_codes:
            raise Exception('Invalid value ' + self.value + ' must be one of: ' + str(option_codes))

    def definition(self):
        output = super().definition()
        output['options'] = [option.to_json() for option in self.options]
        return output

class SelectOption:

    def __init__(self, code, display):
        self.code = code
        self.display = display

    def to_json(self):
        return {
            'code': self.code,
            'display': self.display,
        }
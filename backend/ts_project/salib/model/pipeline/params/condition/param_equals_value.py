from .param_condition import ParamCondition

class ParamEqualsValue(ParamCondition):

    def __init__(self, param, value):
        self.param = param
        self.value = value

    def is_valid(self, all_params):
        return all_params[self.param].value == self.value

    def to_json(self):
        return {
            'type': 'param_equals_value',
            'args': {
                'param': self.param,
                'value': self.value
            }
        }
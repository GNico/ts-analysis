from param_condition import ParamCondition

class ParamEqualsValue(ParamCondition):

    def __init__(self, param, value):
        self.param = param
        self.value = value

    def to_json(self):
        return {
            'type': 'param_equals_value',
            'args': {
                'param': self.param,
                'value': self.value
            }
        }
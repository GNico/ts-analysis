class ParamCondition:

    def to_json(self):
        raise Exception('Undefined to_json for: ' + type(self).__name__)

    def is_valid(self, all_params):
        raise Exception('Undefined is_valid for: ' + type(self).__name__)
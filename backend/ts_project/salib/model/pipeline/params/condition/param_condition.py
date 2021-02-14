class ParamCondition:

    def to_json(self):
        raise Exception('Undefined to_json for: ' + type(self).__name__)
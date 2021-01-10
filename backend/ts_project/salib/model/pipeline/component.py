import copy

class Component:

    def __init__(self):
        self.params = {}
        self.required_params = {}

    def add_required_param(self, param):
        self.required_params[param.id] = param

    def set_param(self, param):
        self.params[param.id] = param

    def set_param_value(self, id, value):
        new_param = copy.deepcopy(self.get_param(id))
        new_param.value = value
        self.set_param(new_param)

    def get_param(self, id):
        if id in self.params: 
            return self.params[id]
        elif id in self.required_params:
            return self.required_params[id]
        else:
            raise 'Invalid param ' + id


    def params_definition(self):
        output = {}
        for id, param in self.required_params.items():
            output[id] = param.definition()
        return output

    def validate(self):
        for required_param in self.required_params.values():
            if required_param.id not in self.params:
                raise Exception('Missing required param ' + required_param)
            if required_param.klass != self.params[required_param.id].klass:
                raise Exception('Invalid type for ' + required_param.id + ', expected ' + required_param.klass + 
                                ' but was ' + self.params[required_param.id].klass)
        for param in self.params.values():
            param.validate()

    def id(self):
        raise Exception('Undefined id')
from collections import OrderedDict
import copy

class Node:

    def __init__(self, id):
        self.id = id
        self.required_params = OrderedDict()
        self.params = OrderedDict()
        self.sources = []
        self.input_names = []

    def display(self):
        raise Exception('Undefined display name: ' + type(self).__name__)

    def desc(self):
        raise Exception('Undefined description: ' + type(self).__name__)

    def execute(self, inputs):
        raise Exception('Unimplemented execution: ' + type(self).__name__)

    def add_source(self, source):
        self.sources.append(source)

    def node_sources(self):
        return list(filter(lambda x: x.is_node_ref(), self.sources))

    def input_sources(self):
        return list(filter(lambda x: x.is_node_ref(), self.sources))

    def sources(self):
        return self.sources

    def add_param(self, param):
        self.params[param.id] = param

    def add_required_param(self, param):
        self.required_params[param.id] = param

    def set_param(self, param):
        self.params[param.id] = param

    def set_param_value(self, id, value):
        new_param = copy.deepcopy(self.get_param(id))
        new_param.value = value
        self.set_param(new_param)

    def validate_inputs(self, inputs):
        num_required_inputs = self.num_required_inputs()
        if num_required_inputs is not None:
            num_inputs = len(inputs)
            if num_inputs != num_required_inputs:
                raise ValueError("Node %s must have %s inputs, %s given" %(self.id, num_required_inputs, num_inputs))

    def num_required_inputs(self):
        count = len(self.input_names)
        return None if count == 0 else count

    def set_input_names(self, input_names):
        self.input_names = input_names

    def inputs_definition(self):
        return {
            'num_required_inputs': self.num_required_inputs(),
            'names': self.input_names
        }

    def get_param(self, id):
        if id in self.params: 
            return self.params[id]
        elif id in self.required_params:
            return self.required_params[id]
        else:
            raise Exception('Invalid param ' + id)

    def params_definition(self):
        output = []
        for id, param in self.required_params.items():
            output.append(param.definition())
        for id, param in self.params.items():
            output.append(param.definition())
        return output

    def validate(self):
        for required_param in self.required_params.values():
            if required_param.id not in self.params:
                raise Exception('Missing required param ' + required_param.id)
            if required_param.type != self.params[required_param.id].type:
                raise Exception('Invalid type for ' + required_param.id + ', expected ' + required_param.type + 
                                ' but was ' + self.params[required_param.id].type)
        for param in self.params.values():
            param.validate()

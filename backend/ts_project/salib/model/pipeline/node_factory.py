from .nodes.detectors.ema import EMA

class NodeFactory:

    NODE_TYPES = {
        'transformer': {

        },
        'detector': {
            'EMA': EMA
        },
        'aggregator': {

        }
    }

    @staticmethod
    def base_node(klass, type):
        if klass in NodeFactory.NODE_TYPES.keys():
            if type in NodeFactory.NODE_TYPES[klass].keys():
                return NodeFactory.NODE_TYPES[klass][type]()
            else:
                raise Exception('Invalid node type ' + type)
        else:
            raise Exception('Invalid node class ' + type)

    @staticmethod
    def nodes_description(klass):
        output = []
        for type in NodeFactory.NODE_TYPES[klass]:
            instance = NodeFactory.base_node(klass, type)
            entry = {}
            entry['class'] = klass
            entry['type'] = type
            entry['desc'] = instance.desc()
            entry['params'] = instance.params_definition()
            output.append(entry)
        return output

    @staticmethod
    def detectors_description():
        return NodeFactory.nodes_description('detector')

    @staticmethod
    def transformers_description():
        return NodeFactory.nodes_description('transformer')

    @staticmethod
    def aggregators_description():
        return NodeFactory.nodes_description('aggregator')

    @staticmethod
    def detector(type):
        return NodeFactory('detector', type)

    @staticmethod
    def transformer(type):
        return NodeFactory('transformer', type)

    @staticmethod
    def aggregator(type):
        return NodeFactory('aggregator', type)

    def __init__(self, klass, type):
        self.node = NodeFactory.base_node(klass, type)

    def set_param_value(self, id, value):
        self.node.set_param_value(id, value)
        return self

    def build(self):
        self.node.validate()
        return self.node
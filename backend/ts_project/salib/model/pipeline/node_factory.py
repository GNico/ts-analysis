from .nodes.transformers.ema import EMA
from .nodes.transformers.std_normalize import StdNormalize
from .nodes.transformers.rolling_aggregate_mean import RollingAggregateMean

from .nodes.detectors.simple_threshold import SimpleThreshold

from .nodes.aggregators._and import And
from .nodes.aggregators._or import Or

class NodeFactory:

    NODE_TYPES = {
        'transformer': {
            'StdNormalize': StdNormalize,
            'EMA': EMA,
            'RollingAggregateMean': RollingAggregateMean
        },
        'detector': {
            'SimpleThreshold': SimpleThreshold
        },
        'aggregator': {
            'OR': Or,
            'AND': And
        }
    }

    @staticmethod
    def base_node(id, group, type):
        if group in NodeFactory.NODE_TYPES.keys():
            if type in NodeFactory.NODE_TYPES[group].keys():
                return NodeFactory.NODE_TYPES[group][type](id)
            else:
                raise Exception('Invalid node type ' + type)
        else:
            raise Exception('Invalid node group ' + type)

    @staticmethod
    def nodes_description(group):
        output = []
        for type in NodeFactory.NODE_TYPES[group]:
            instance = NodeFactory.base_node(None, group, type)
            entry = {}
            entry['type'] = type
            entry['group'] = group
            entry['desc'] = instance.desc()
            entry['display'] = instance.display()
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
    def detector(id, type):
        return NodeFactory(id, 'detector', type)

    @staticmethod
    def transformer(id, type):
        return NodeFactory(id, 'transformer', type)

    @staticmethod
    def aggregator(id, type):
        return NodeFactory(id, 'aggregator', type)

    @staticmethod
    def from_json(obj):
        id = obj['id']
        group = obj['group']
        type = obj['type']
        builder = NodeFactory(id, group, type)
        if 'params' in obj.keys():
            params = obj['params']
            for param in params:
                builder.set_param_value(param['id'], param['value'])
        if 'sources' in obj.keys():
            sources = obj['sources']
            for source in sources:
                builder.add_source(source)
        return builder.build()

    def __init__(self, id, group, type):
        self.node = NodeFactory.base_node(id, group, type)

    def set_param_value(self, id, value):
        if value == '':
            value = None
        self.node.set_param_value(id, value)
        return self

    def add_source(self, source):
        self.node.add_source(source)
        return self

    def build(self):
        self.node.validate()
        return self.node
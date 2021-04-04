from .nodes.transformers.ema import EMA
from .nodes.transformers.difference import Difference
from .nodes.transformers.std_normalize import StdNormalize
from .nodes.transformers.shift import Shift
from .nodes.transformers.identity import Identity
from .nodes.transformers.rolling_aggregate import RollingAggregate

from .nodes.detectors.simple_threshold import SimpleThreshold
from .nodes.detectors.interquartile_range import InterQuartileRange
from .nodes.detectors.quantile import Quantile

from .nodes.aggregators.union import Union
from .nodes.aggregators.intersect import Intersect

class NodeFactory:

    NODE_TYPES = {
        'transformer': {
            'StdNormalize': StdNormalize,
            'Shift': Shift,
            'Identity': Identity,
            'EMA': EMA,
            'Difference': Difference,
            'RollingAggregate': RollingAggregate,
        },
        'detector': {
            'SimpleThreshold': SimpleThreshold,
            'Quantile': Quantile,
            'InterQuartileRange': InterQuartileRange
        },
        'aggregator': {
            'Union': Union,
            'Intersect': Intersect,
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
    def node_description(group, type):
        instance = NodeFactory.base_node(None, group, type)
        entry = {}
        entry['type'] = type
        entry['group'] = group
        entry['desc'] = instance.desc()
        entry['display'] = instance.display()
        entry['params'] = instance.params_definition()
        return entry

    @staticmethod
    def nodes_list():
        output = {}
        for group, types in NodeFactory.NODE_TYPES.items():
            nodes = []
            for type in types:
                instance = NodeFactory.base_node(None, group, type)
                entry = {}
                entry['type'] = type
                entry['desc'] = instance.desc()
                entry['display'] = instance.display()
                entry['params'] = instance.params_definition()
                entry['inputs'] = instance.inputs_definition()
                nodes.append(entry)
            output[group] = nodes
        return output

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
        if obj.get('debug') is True:
            builder.set_debug(True)
        return builder.build()

    def __init__(self, id, group, type):
        self.node = NodeFactory.base_node(id, group, type)

    def set_param_value(self, id, value):
        if value == '':
            value = None
        self.node.set_param_value(id, value)
        return self

    def set_debug(self, value):
        self.node.set_debug(value)

    def add_source(self, source):
        self.node.add_source(source)
        return self

    def build(self):
        self.node.validate()
        return self.node
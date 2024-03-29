import numpy as np

from .nodes.transformers.clamp import Clamp
from .nodes.transformers.sigmoid import Sigmoid
from .nodes.transformers.rescale import Rescale
from .nodes.transformers.exponential_moving_average import ExponentialMovingAverage
from .nodes.transformers.exponential_smoothing import ExponentialSmoothing
from .nodes.transformers.difference import Difference
from .nodes.transformers.derivative import Derivative
from .nodes.transformers.divide import Divide
from .nodes.transformers.std_normalize import StdNormalize
from .nodes.transformers.abs_value import AbsValue
from .nodes.transformers.shift import Shift
from .nodes.transformers.boxcox import BoxCox
from .nodes.transformers.identity import Identity
from .nodes.transformers.fft_filter import FFTFilter
from .nodes.transformers.rolling_aggregate import RollingAggregate
from .nodes.transformers.dropout import Dropout
from .nodes.transformers.multi_rolling_aggregate import MultiRollingAggregate
from .nodes.transformers.stl import STL
from .nodes.transformers.seasonal_decompose import SeasonalDecompose
from .nodes.transformers.auto_regression import AutoRegression
from .nodes.transformers.markov_auto_regression import MarkovAutoRegression
from .nodes.transformers.sarimax import SARIMAX
from .nodes.transformers.var import VAR
from .nodes.transformers.garch import GARCH
from .nodes.transformers.alma import ALMA

from .nodes.detectors.simple_threshold import SimpleThreshold
from .nodes.detectors.quantile import Quantile

from .nodes.aggregators.union import Union
from .nodes.aggregators.slack import Slack
from .nodes.aggregators.intersect import Intersect

from .nodes.node_source import NodeSourceParser

class NodeFactory:

    def __init__(self, node_id, group, type):
        self.node = NodeFactory.base_node(node_id, group, type)

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

    NODE_TYPES = {
        'transformer': {
            'Identity': Identity,
            'Shift': Shift,
            'StdNormalize': StdNormalize,
            'Clamp': Clamp,
            'Rescale': Rescale,
            'AbsValue': AbsValue,
            'Sigmoid': Sigmoid,
            'ExponentialMovingAverage': ExponentialMovingAverage,
            'ExponentialSmoothing': ExponentialSmoothing,
            'Difference': Difference,
            'Derivative': Derivative,
            'Divide': Divide,
            'RollingAggregate': RollingAggregate,
            'MultiRollingAggregate': MultiRollingAggregate,
            'Dropout': Dropout,
            'BoxCox': BoxCox,
            'STL': STL,
            'Seasonal decompose': SeasonalDecompose,
            'AutoRegression': AutoRegression,
            'MarkovAutoRegression': MarkovAutoRegression,
            'FFTFilter': FFTFilter,
            'SARIMAX': SARIMAX,
            'VAR': VAR,
            'ALMA': ALMA,
            'GARCH': GARCH,
        },
        'detector': {
            'SimpleThreshold': SimpleThreshold,
            'Quantile': Quantile
        },
        'aggregator': {
            'Union': Union,
            'Intersect': Intersect,
            'Slack': Slack
        }
    }

    @staticmethod
    def base_node(node_id, group, type):
        if group in NodeFactory.NODE_TYPES.keys():
            if type in NodeFactory.NODE_TYPES[group].keys():
                constructor = NodeFactory.NODE_TYPES[group][type]
                new_node = constructor(node_id)
                return new_node
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
            sorted_types = {k: v for k, v in sorted(types.items(), key=lambda i: i[1].display(i[1]))}
            for type in sorted_types:
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
        try:
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
                    builder.add_source(NodeSourceParser.parse(source))
            return builder.build()
        except Exception as e:
            raise RuntimeError('Error parsing node `' + str(obj) + '`') from e
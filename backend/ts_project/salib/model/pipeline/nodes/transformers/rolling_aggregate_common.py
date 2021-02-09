from ...params.string import String
from ...params.boolean import Boolean
from ...params.int import BoundedInt

class RollingAggregateCommon:

    @staticmethod
    def add_common_params(node):
        node.add_required_param(String('window', 'Window', 'Window size in time interval (eg: 1h)', '30m'))
        node.add_required_param(Boolean('center', 'Center', 'Center aggregation window around value', False))
        node.add_param(BoundedInt('min_periods', 'Min. periods', 'Min number of periods', 0, None))

    @staticmethod
    def get_common_params(node):
        window = node.get_param('window').value
        center = node.get_param('center').value
        min_periods = node.get_param('min_periods').value
        return (window, center, min_periods)

    @staticmethod
    def str_params(node):
        return ','.join(map(lambda p: str(p), RollingAggregateCommon.get_common_params(node)))
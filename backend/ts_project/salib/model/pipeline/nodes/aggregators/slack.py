from ..node import Node
from ..node_result import NodeResult
from ...params.boolean import Boolean
from ...params.string import String
from ....anomaly import Anomaly

class Slack(Node):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('slack', 'Slack', 'Anomaly extension: can be interval, period or %', '25%'))

    def execute(self, inputs, debug):
        if len(inputs) == 1:
            all_anomalies = inputs.anomalies
        else:
            all_anomalies = inputs[0].anomalies
            for i in inputs[1:]:
                all_anomalies = self.join(all_anomalies, i.anomalies)
        return NodeResult(self, inputs=inputs, anomalies=all_anomalies)

    def join(self, lhss, rhss):
        raise ValueError('ToDo')

    def __str__(self):
        return 'Slack(' + self.get_param('slack').value + ')[' + self.id + ']'

    def desc(self):
        return 'Extend anomalies and combine'

    def display(self):
        return 'Slack'
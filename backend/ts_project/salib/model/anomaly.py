from functools import total_ordering
import pandas as pd

from .utils import timestamp_to_epoch


@total_ordering
class Anomaly:

    def __init__(self, series, start, end, score, desc=None):
        self.series = series
        self.start = start
        self.end = end
        self.score = score
        self.source_node = None
        self.desc = desc

    def output_format(self):
        from_timestamp = timestamp_to_epoch(self.start)
        to_timestamp = timestamp_to_epoch(self.end)
        return {
            "from": from_timestamp,
            "to": to_timestamp,
            "score": self.score,
            "desc": self.desc,
            "source_node": self.source_node_id()
        }

    def source_node_id(self):
        if self.source_node is not None:
            return self.source_node.id
        else:
            return None

    def set_source_node(self, source_node):
        self.source_node = source_node

    @staticmethod
    def from_epoch(series, start, end, score, desc=None):
        start_t = pd.Timestamp(start, unit='s')
        end_t = pd.Timestamp(end, unit='s')
        return Anomaly(series, start_t, end_t, score, desc)

    def __hash__(self):
        return hash(self.start) + hash(self.end) + hash(self.score)

    def __eq__(self, other):
        return \
            self.start == other.start and \
            self.end == other.end and \
            self.score == other.score and \
            self.source_node == other.source_node

    def __lt__(self, other):
        return ((self.start, self.end, self.source_node_id()) < (other.start, other.end, self.source_node_id()))

    def __str__(self):
        return str(self.output_format())

    def __repr__(self):
        return self.__str__()
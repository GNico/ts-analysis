import hashlib
import json
from functools import total_ordering

import pandas as pd

from .utils import timestamp_to_epoch


@total_ordering
class Anomaly:

    def __init__(self, series, start, end, score):
        self.series = series
        self.start = start
        self.end = end
        self.score = score
        self.source_node = None
        self.source_anomalies = []

    def id(self):
        id_members = [
            self.start.value,
            self.end.value,
            self.score,
            self.source_node_id(),
            [sa.id() for sa in self.source_anomalies]
        ]
        return hashlib.md5(json.dumps(id_members).encode('utf-8')).hexdigest()

    def output_format(self):
        from_timestamp = timestamp_to_epoch(self.start)
        to_timestamp = timestamp_to_epoch(self.end)
        return {
            "id": self.id(),
            "from": from_timestamp,
            "to": to_timestamp,
            "score": self.score,
            "source_anomalies": [sa.id() for sa in self.source_anomalies],
            "source_node": self.source_node_id()
        }

    def epoch_span(self):
        from_timestamp = timestamp_to_epoch(self.start)
        to_timestamp = timestamp_to_epoch(self.end)
        return (from_timestamp, to_timestamp)

    def epoch_span_secs(self):
        epoch_span_ms = self.epoch_span()
        return tuple(map(lambda x: x//1000, epoch_span_ms))

    def source_node_id(self):
        if self.source_node is not None:
            return self.source_node.id
        else:
            return None

    def set_source_node(self, source_node):
        self.source_node = source_node

    def set_source_anomalies(self, source_anomalies):
        self.source_anomalies = source_anomalies

    @staticmethod
    def from_epoch(series, start, end, score):
        start_t = pd.Timestamp(start, unit='s')
        end_t = pd.Timestamp(end, unit='s')
        return Anomaly(series, start_t, end_t, score)

    def __hash__(self):
        return hash(self.start) + hash(self.end) + hash(self.score) + hash(self.source_node_id())

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
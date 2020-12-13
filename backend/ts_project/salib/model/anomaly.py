from functools import total_ordering
import pandas as pd

from .utils import timestamp_to_epoch


@total_ordering
class Anomaly:

    def __init__(self, series, start, end, score, desc=None):
        self.series = series
        self.start = start
        # inclusive
        self.end = end
        self.score = score
        self.algo_tag = None
        self.desc = desc

    def output_format(self):
        from_timestamp = timestamp_to_epoch(self.start)
        to_timestamp = timestamp_to_epoch(self.end + self.series.step())
        if from_timestamp == to_timestamp:
            print("START", self.start, "END", self.end, "STEP", self.series.step())
        return {
            "from": from_timestamp,
            "to": to_timestamp,
            "score": self.score,
            "desc": self.desc,
            "algo_id": self.algo_tag
        }

    def tag_algo(self, algo_id):
        self.algo_tag = algo_id

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
            self.score == other.score

    def __lt__(self, other):
        return ((self.start, self.end) < (other.start, other.end))

    def __str__(self):
        return str(self.output_format())

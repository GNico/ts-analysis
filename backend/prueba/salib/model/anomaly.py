from functools import total_ordering
import pandas as pd


@total_ordering
class Anomaly:

    def __init__(self, start, end, score):
        self.start = start
        # inclusive
        self.end = end
        self.score = score

    def output_format(self):
        return {
            "from": self.start,
            "to": self.end,
            "score": self.score
        }

    def from_epoch(start, end, score):
        start_t = pd.Timestamp(start, unit='s')
        end_t = pd.Timestamp(end, unit='s')
        return Anomaly(start_t, end_t, score)

    def __hash__(self):
        return hash(self.start) + hash(self.end) + hash(self.score)

    def __eq__(self, other):
        return \
            self.start == other.start and \
            self.end == other.end and \
            self.score == other.score

    def __lt__(self, other):
        return ((self.start, self.end) < (other.start, other.end))

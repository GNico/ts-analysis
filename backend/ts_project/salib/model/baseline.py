from .utils import timestamp_to_epoch

class Baseline:

  def __init__(self):
    self.data = []

  def add_point(self, timestamp, low, high):
    self.data.append([timestamp, low, high])

  def output_format(self):
    return list(map(lambda e: [timestamp_to_epoch(e[0]), e[1], e[2]], self.data))
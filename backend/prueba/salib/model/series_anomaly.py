class SeriesAnomaly:

  def __init__(self, start, end, score):
    self.start = start
    self.end = end
    self.score = score

  def output_format(self):
    return {
      "from": self.start,
      "to": self.end,
      "score": self.score
    }
  
  def __hash__(self):
    return hash(self.start) + hash(self.end) + hash(self.score)

  def __eq__(self, other):
    return self.start == other.start and self.end == other.end and self.score == other.score
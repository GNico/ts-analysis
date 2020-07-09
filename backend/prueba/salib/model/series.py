class Series:

    def __init__(self, pdseries, interval):
        self.pdseries = pdseries
        self.start = pdseries[0]
        self.end = pdseries[-1]
        self.interval = interval

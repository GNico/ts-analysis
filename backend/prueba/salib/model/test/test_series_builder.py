from model import series


class TestSeriesBuilder:

    def __init__(self, data, interval=1, unit='s'):
        self.unit = unit
        self.interval = interval
        self.data = data

    def assert_same_units(self, other):
        if self.unit != other.unit or self.interval != other.interval:
            raise ValueError('Unit/interval mismatch')

    def append(self, test_series):
        self.assert_same_units(test_series)
        last_index = self.data[-1][0] + 1
        first_new_index = test_series.data[0][0]
        for e in test_series.data:
            new_index = last_index + e[0] - first_new_index
            entry = e[1]
            self.data.append([new_index, entry])

    def compose(self, test_series):
        self.assert_same_units(test_series)
        for i in range(len(self.data)):
            index = self.data[i][0]
            self.data[i] = [index, self.data[i][1] + test_series.data[i][1]]

    def build(self):
        return series.Series.from_array(self.data, self.interval, self.unit)

    @staticmethod
    def constant(length, value=0, interval=1, unit='s'):
        return TestSeriesBuilder.linear(length, value, 0, interval, unit)

    @staticmethod
    def linear(length, startvalue, slope, interval=1, unit='s'):
        data = []
        for i in range(length):
            data.append([i*interval, startvalue + slope*i*interval])
        return TestSeriesBuilder(data, interval, unit)

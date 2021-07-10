import numpy as np
import pandas as pd
from math import exp

from ....utils import timedelta_to_period
from ..node_transformer import NodeTransformer
from ...params.string import String

class ALMA(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(String('window', 'Window', 'Window size in periods or time interval (eg: 12h)', '12h'))

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        window = self.window(series.step())
        self._alma_weights = self.alma_weights(window=window)
        alma = pdseries.rolling(window=window).apply(self.calculate_alma, args=(window,), raw=False).dropna()
        return (pd.Series(alma, name=f'alma'), {})

    def calculate_alma(self, s, window):
        weights = self._alma_weights
        if len(s) < window:
            return None
        else:
            weighted_sum = weights * s
            alma = weighted_sum.sum() / weights.sum()
            return alma
    
    def alma_weights(self, window, offset=0.85, sigma=6):
        m = int(offset * (window - 1))
        s = (window/sigma)
        k_all = list(range(0, window))
        weights = []
        for k in k_all:
            wtd = exp(-((k-m)**2)/(2*(s**2)))
            weights.append(wtd)
        return np.array(weights)

    def window(self, base_step):
        return timedelta_to_period(self.get_param('window').value, base_step)

    def __str__(self):
        return "ALMA(" + str(self.get_param('window').value) + ")[" + self.id + "]"

    def display(self):
        return 'Arnaud Legoux moving average'

    def desc(self):
        return 'Arnaud Legoux moving average'

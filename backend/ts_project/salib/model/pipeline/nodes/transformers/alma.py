import numpy as np
import pandas as pd
from math import exp

from ..node_transformer import NodeTransformer
from ...params.int import BoundedInt

class ALMA(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(BoundedInt('window', 'Window', 'Window size', 0, None, 24))

    def transform(self, seriess):
        pdseries = seriess[0].pdseries
        window = self.window()
        self._alma_weights = self.alma_weights(window=window)
        alma = pdseries.rolling(window=window).apply(self.calculate_alma, raw=False).dropna()
        return pd.Series(alma, name=f'alma')

    def calculate_alma(self, s):
        weights = self._alma_weights
        if len(s) < self.window():
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

    def window(self):
        return self.get_param('window').value

    def __str__(self):
        return "ALMA(" + str(self.window()) + ")[" + self.id + "]"

    def display(self):
        return 'Arnaud Legoux moving average'

    def desc(self):
        return 'Arnaud Legoux moving average'

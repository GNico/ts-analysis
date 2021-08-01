import pandas as pd
import numpy as np

from ..node_transformer import NodeTransformer
from ...params.string import String
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ....utils import timedelta_to_period

class FFTFilter(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(Boolean('inside', 'Inside', 'If true, freq must be within bounds', True))
        self.add_required_param(Boolean('strict', 'Strict', 'Strict comparison on bounds', False))
        self.add_param(BoundedInt('lower', 'Lower', 'Lower bound', 0, None, 0))
        self.add_param(BoundedInt('upper', 'Upper', 'Upper bound', 0, None, 0))

    def get_params(self):
        lower = self.get_param('lower').value
        upper = self.get_param('upper').value
        inside = self.get_param('inside').value
        strict = self.get_param('strict').value
        return (lower, upper, inside, strict)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        lower, upper, inside, strict = self.get_params()
        # calc_lags = timedelta_to_period(lags, series.step())
        n = len(pdseries)
        fhat = np.fft.fft(pdseries, n)
        PSD = fhat * np.conj(fhat) / n
        freqs = np.fft.fftfreq(n, 1)

        # Debug info
        if debug:
            fft_chart = []
            for i in range(0, len(freqs)//2):
                fft_chart.append([freqs[i], PSD[i].real])
            debug_info = {
                "fft_chart": fft_chart
            }
        else:
            debug_info = {}

        adj = 0.05
        indices = ([True] * int(len(fhat)*adj)) + ([False] * int((len(fhat)+1)*(1-adj)))
        fhat = indices * fhat
        inverse_values = np.fft.ifft(fhat)
        output = pd.Series(inverse_values, index=pdseries.index)
        return (output, debug_info)

    def __str__(self):
        return "FFTFilter" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'FFT filter'

    def desc(self):
        return 'Fast Fourier Transform band pass filter'

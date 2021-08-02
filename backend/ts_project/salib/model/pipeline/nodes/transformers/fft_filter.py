import pandas as pd
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq

from ..node_transformer import NodeTransformer
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class FFTFilter(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_params()

    def add_params(self):
        self.add_required_param(String('cutoff', 'Power cutoff', 'Power value or percentile cutoff for bandpass. Eg: 500 or 50%', '95%'))
        output_options = [
            SelectOption("filtered", "Filtered"),
            SelectOption("resid", "Residual"),
        ]
        self.add_required_param(Select('output', 'Output', 'Output filtered signal or residuals', output_options, output_options[0].code))

    def get_params(self):
        cutoff = self.get_param('cutoff').value
        output = self.get_param('output').value
        return (cutoff, output)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries

        cutoff, output = self.get_params()
        n = len(pdseries)
        fhat = fft(pdseries, n)
        freqs = fftfreq(n, 1)
        powers = np.abs(fhat)

        if cutoff[-1] == '%':
            cutoff_value = np.percentile(powers, float(cutoff[:-1]))
        else:
            cutoff_value = float(cutoff)

        if output == 'filtered':
            fhat[(powers>=cutoff_value)] = 0
        elif output == 'resid':
            fhat[(powers<=cutoff_value)] = 0
        else:
            raise ValueError('Invalid output: ' + output)
        inverse_values = np.abs(ifft(fhat))
        # Debug info
        if debug:
            fft_chart = []
            for i in range(0, min(1000, len(freqs)//2)):
                fft_chart.append([freqs[i], powers[i]])
            debug_info = {
                "fft_chart": fft_chart,
                "cutoff": cutoff_value,
            }
        else:
            debug_info = {}

        output = pd.Series(inverse_values, index=pdseries.index)
        return (output, debug_info)

    def __str__(self):
        return "FFTFilter" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'FFT filter'

    def desc(self):
        return 'Fast Fourier Transform band pass filter'

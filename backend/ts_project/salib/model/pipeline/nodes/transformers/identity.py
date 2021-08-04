import numpy as np
import statsmodels.tsa.stattools as stattools
import scipy

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
from ...params.int import BoundedInt
from ...params.string import String
from ....utils import timedelta_to_period
from ...params.condition.param_equals_value import ParamEqualsValue

class Identity(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('mean', 'Mean', 'Series mean', False))
        self.add_required_param(Boolean('stddev', 'Std. deviation', 'Series standard deviation', False))
        self.add_required_param(Boolean('adf_test', 'ADF test', 'Augmented Dicky-Fuller test', False))
        self.add_required_param(Boolean('normality_test', 'Normal test', 'Normality test', False))

        self.add_required_param(Boolean('histogram', 'Histogram', 'Histogram plot', False))
        histogram_bins = BoundedInt('histogram_bins', 'Histogram bins', 'Number of equal spaced bins in histogram', 2, None, 25)
        histogram_bins.add_condition(ParamEqualsValue('histogram', True))
        self.add_required_param(histogram_bins)

        self.add_required_param(Boolean('cum_histogram', 'Cum. Histogram', 'Cumulative histogram plot', False))
        cum_histogram_bins = BoundedInt('cum_histogram_bins', 'Cum. Histogram bins', 'Number of equal spaced bins in cumulative histogram', 2, None, 25)
        cum_histogram_bins.add_condition(ParamEqualsValue('cum_histogram', True))
        self.add_required_param(cum_histogram_bins)

        self.add_required_param(Boolean('acf', 'ACF', 'Autocorrelation function', False))
        acf_lags = String('acf_lags', 'ACF lags', 'ACF max lags', '7d')
        acf_lags.add_condition(ParamEqualsValue('acf', True))
        self.add_required_param(acf_lags)

        self.add_required_param(Boolean('pacf', 'PACF', 'Partial autocorrelation function', False))
        pacf_lags = String('pacf_lags', 'PACF lags', 'PACF max lags', '7d')
        pacf_lags.add_condition(ParamEqualsValue('pacf', True))
        self.add_required_param(pacf_lags)

    def transform(self, seriess, debug):
        series = seriess[0]
        pdseries = series.pdseries
        if debug:
            debug_info = {}
            if self.get_param('mean').value:
                debug_info['Mean'] = pdseries.mean()
            if self.get_param('stddev').value:
                debug_info['Std. dev.'] = pdseries.std()
            if self.get_param('stddev').value:
                debug_info['Std. dev.'] = pdseries.std()
            if self.get_param('adf_test').value:
                self.update_debug_info(debug_info, 'ADF', self.adf_test(pdseries))
            if self.get_param('normality_test').value:
                mean = pdseries.mean()
                std = pdseries.std()
                std = 1 if std == 0 else std
                std_series = (pdseries - mean) / std
                _, normality_p_value = scipy.stats.normaltest(std_series, nan_policy='omit')
                debug_info['Normality: rejection p-value'] = normality_p_value
            if self.get_param('histogram').value:
                self.update_debug_info(debug_info, 'Histogram', self.histogram(pdseries))
            if self.get_param('cum_histogram').value:
                self.update_debug_info(debug_info, 'Cum. Histogram', self.cum_histogram(pdseries))
            if self.get_param('acf').value:
                self.update_debug_info(debug_info, 'ACF', self.acf(series))
            if self.get_param('pacf').value:
                self.update_debug_info(debug_info, 'PACF', self.pacf(series))
        else:
            debug_info = {}    
        return (pdseries, debug_info)

    def update_debug_info(self, debug_info, prefix, to_merge):
        for k, v in to_merge.items():
            debug_info[prefix + ': ' + k] = v

    def acf(self, series):
        pdseries = series.pdseries
        calc_lags = timedelta_to_period(self.get_param('acf_lags').value, series.step())
        nlags = min(len(pdseries) // 2 - 1, calc_lags)
        acf_result = stattools.acf(pdseries, nlags=nlags, fft=True)
        coeffs = acf_result.tolist()
        acf_plot = []
        for i in range(1, len(coeffs)):
            acf_plot.append([i, coeffs[i]])
        return {'lag_correlations_chart': acf_plot}

    def pacf(self, series):
        pdseries = series.pdseries
        calc_lags = timedelta_to_period(self.get_param('pacf_lags').value, series.step())
        nlags = min(len(pdseries) // 2 - 1, calc_lags)
        pacf_result = stattools.pacf(pdseries, nlags=nlags, method='ols')
        coeffs = pacf_result.tolist()
        pacf_plot = []
        for i in range(1, len(coeffs)):
            pacf_plot.append([i, coeffs[i]])
        return {'lag_correlations_chart': pacf_plot}

    def adf_test(self, pdseries):
        debug_info = {}
        dftest = stattools.adfuller(pdseries, autolag='AIC')
        debug_info['Test Statistic'] = dftest[0]
        # Must be below significant level (.05) for stationarity
        debug_info['p-value'] = dftest[1]
        debug_info['# lags used'] = dftest[2]
        debug_info['Observations'] = int(dftest[3])
        for key,value in dftest[4].items():
            # Test statistic must be below critical level for stationarity
            debug_info['Critical Value (%s)'%key] = value
        return debug_info

    def histogram(self, pdseries):
        plot = []
        count, division = np.histogram(pdseries, bins=self.get_param('histogram_bins').value)
        for i in range(len(count)):
            plot.append([float(division[i]), float(count[i])])
        return {'chart': plot}

    def cum_histogram(self, pdseries):
        plot = []
        count, division = np.histogram(pdseries, bins=self.get_param('cum_histogram_bins').value)
        cumsum = np.cumsum(count)
        for i in range(len(cumsum)):
            plot.append([float(division[i]), float(cumsum[i])])
        return {'chart': plot}

    def __str__(self):
        return "Identity[" + self.id + "]"

    def display(self):
        return 'Identity/probe'

    def desc(self):
        return 'Identity - no transformation. Use to probe series.'

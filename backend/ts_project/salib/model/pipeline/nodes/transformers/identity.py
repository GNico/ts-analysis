import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
from ...params.int import BoundedInt

class Identity(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('adf_test', 'ADF test', 'Include Augmented Dicky-Fuller test', True))
        self.add_required_param(Boolean('acf', 'ACF', 'Autocorrelation function', True))
        self.add_required_param(BoundedInt('acf_lags', 'ACF lags', 'ACF max lags', 0, None, 10))
        self.add_required_param(Boolean('pacf', 'PACF', 'Partial autocorrelation function', True))
        self.add_required_param(BoundedInt('pacf_lags', 'PACF lags', 'PACF max lags', 0, None, 10))
        self.add_required_param(Boolean('mean', 'Mean', 'Series mean', True))
        self.add_required_param(Boolean('stddev', 'Std. deviation', 'Series standard deviation', True))
        
    def transform(self, seriess, debug):
        pdseries = seriess[0].pdseries
        if debug:
            debug_info = {}
            if self.get_param('adf_test').value:
                self.update_debug_info(debug_info, 'ADF', self.adf_test(pdseries))
            if self.get_param('acf').value:
                self.update_debug_info(debug_info, 'ACF', self.acf(pdseries))
            if self.get_param('pacf').value:
                self.update_debug_info(debug_info, 'PACF', self.pacf(pdseries))
            if self.get_param('mean').value:
                debug_info['Mean'] = pdseries.mean()
            if self.get_param('stddev').value:
                debug_info['Std. dev.'] = pdseries.std()
        else:
            debug_info = {}    
        return (pdseries, debug_info)

    def update_debug_info(self, debug_info, prefix, to_merge):
        for k, v in to_merge.items():
            debug_info[prefix + ': ' + k] = v

    def acf(self, pdseries):
        nlags = min(len(pdseries) // 2 - 1, self.get_param('acf_lags').value)
        acf_result = stattools.acf(pdseries, nlags=nlags, fft=True)
        coeffs = acf_result.tolist()
        acf_plot = []
        for i in range(len(coeffs)):
            acf_plot.append([i, coeffs[i]])
        return {'lag_correlations': acf_plot}

    def pacf(self, pdseries):
        nlags = min(len(pdseries) // 2 - 1, self.get_param('pacf_lags').value)
        pacf_result = stattools.pacf(pdseries, nlags=nlags, method='ols')
        coeffs = pacf_result.tolist()
        pacf_plot = []
        for i in range(len(coeffs)):
            pacf_plot.append([i, coeffs[i]])
        return {'lag_correlations': pacf_plot}

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

    def __str__(self):
        return "Identity[" + self.id + "]"

    def display(self):
        return 'Identity/probe'

    def desc(self):
        return 'Identity - no transformation. Use to probe series.'

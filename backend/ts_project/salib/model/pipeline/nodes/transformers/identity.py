import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
        
class Identity(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.add_required_param(Boolean('adf_test', 'ADF test', 'Include Augmented Dicky-Fuller test', True))
        self.add_required_param(Boolean('acf', 'ACF', 'Autocorrelation function', True))
        self.add_required_param(Boolean('pacf', 'PACF', 'Partial autocorrelation function', True))

        
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
        else:
            debug_info = {}    
        return (pdseries, debug_info)

    def update_debug_info(self, debug_info, prefix, to_merge):
        for k, v in to_merge.items():
            debug_info[prefix + ': ' + k] = v

    def acf(self, pdseries):
        nlags = min(len(pdseries) // 2 - 1, 40)
        acf_result = stattools.acf(pdseries, nlags=nlags, fft=True)
        return {'lag_correlations': acf_result.tolist()}

    def pacf(self, pdseries):
        nlags = min(len(pdseries) // 2 - 1, 40)
        pacf_result = stattools.pacf(pdseries, nlags=nlags, method='ols')
        return {'lag_correlations': pacf_result.tolist()}

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
        return 'Identity'

    def desc(self):
        return 'Identity - apply no transformation'

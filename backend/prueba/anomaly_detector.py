import numpy as np
import pandas as pd
from scipy import stats
from stldecompose import decompose, forecast
from statsmodels.tsa.seasonal import seasonal_decompose

# import importlib
# detector = importlib.import_module('thermometr')

from . import thermometr

def ESaggregationToPandasSeries(response):
	dates = []
	count = []
	for element in response['aggregations']['my_aggregation']['buckets']:
	    dates.append(pd.to_datetime(element['key_as_string']))
	    count.append(element['doc_count'])
	    
	return pd.Series(count, index=dates)

def detectAnomalies(response):

	ts = ESaggregationToPandasSeries(response)

	stl = decompose(ts, period=336)  #una semana periodicidad

	det = thermometr.Thermometr(ts)
	res = det.detect()

	resFormatted = []


	for dic_item in res:
		resFormatted.append([ts.index[dic_item['index']].value // 10 ** 6, dic_item['ESD'] ])

	return resFormatted
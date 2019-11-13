import numpy as np
import pandas as pd
from scipy import stats
from stldecompose import decompose, forecast
from statsmodels.tsa.seasonal import seasonal_decompose


from . import thermometr

def SeriesArrayToPandasSeries(series):
    dates, count = zip(*series)
    dates = pd.to_datetime(dates,unit='ms')
    return pd.Series(count, index=dates)


def detectAnomalies(series):
    ts = SeriesArrayToPandasSeries(series)
    stl = decompose(ts, period=336)  #una semana periodicidad
    det = thermometr.Thermometr(ts)
    result = det.detect()
    formattedResult = []
    for dic_item in result:
        formattedResult.append([ts.index[dic_item['index']].value // 10 ** 6, dic_item['ESD'] ])

    return formattedResult




def testAlgorythms(series):
    pdseries = SeriesArrayToPandasSeries(series)
    anomalies = []

    stlresult = testSTL(pdseries)
    anomalies.append(stlresult)
    results = { "series": series, "results": anomalies }
    return results;


##--------algorythms ------------------

def testSTL(pdseries):
    det = thermometr.Thermometr(pdseries)
    result = det.detect()
    formattedResult = []

    first = (pdseries.index[0].value // 10 ** 6)
    second = (pdseries.index[1].value // 10 ** 6)
    interval = (second - first)


    for dic_item in result:
        timestamp = pdseries.index[dic_item['index']].value // 10 ** 6
        formattedResult.append({"from": timestamp, "to": timestamp+3600000, "score": dic_item['ESD'] })

    response = { "name": "STL thermometr", "data": [], "anomalies": formattedResult }
    return response
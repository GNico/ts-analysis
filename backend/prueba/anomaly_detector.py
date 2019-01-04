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
    res = det.detect()

    resFormatted = []


    for dic_item in res:
        resFormatted.append([ts.index[dic_item['index']].value // 10 ** 6, dic_item['ESD'] ])

    return resFormatted
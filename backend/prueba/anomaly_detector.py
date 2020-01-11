import numpy as np
import pandas as pd
from scipy import stats
from stldecompose import decompose, forecast
from statsmodels.tsa.seasonal import seasonal_decompose

import random
import copy

from . import thermometr

'''
Cada analisis devuelve el siguiente formato, donde cada key es opcional

analysis result format =
{   
    "anomalies": [
        {"start": "timestamp",
        "end": "timestamp",
        "score": 0.0} ],
    "trend": [ ["timestamp", "valor"] ],
    "baseline": {
        [ ["timestamp", "menor valor", "mayor valor"] ]
    }
}
'''

def SeriesArrayToPandasSeries(series):
    dates, count = zip(*series)
    dates = pd.to_datetime(dates,unit='ms')
    return pd.Series(count, index=dates)


def testAlgorythms(series):
    pdseries = SeriesArrayToPandasSeries(series)
    analysis = []
    stlresult = testSTL(pdseries)
    analysis.append(stlresult)

    #adding another analysis for testing
    newanalysis = copy.deepcopy(stlresult)
    newanalysis['name'] = "otro algoritmo"
    #adding random baseline for testing
    newanalysis['results']['baseline'] = generateRandomBaseline(series)
    #adding random trend for testing
    newanalysis['results']['trend'] = generateRandomTrend(pdseries)
    analysis.append(newanalysis)

    analysis_results = { "series": series, "analysis": analysis }

    return analysis_results


##--------algorythms ------------------
def testSTL(pdseries):
    det = thermometr.Thermometr(pdseries)
    anomalies = det.detect()

    first = (pdseries.index[0].value // 10 ** 6)
    second = (pdseries.index[1].value // 10 ** 6)
    interval = (second - first)

    formatted_anomalies = []
    for anomaly in anomalies:
        timestamp = pdseries.index[anomaly['index']].value // 10 ** 6
        formatted_anomalies.append({"from": timestamp, "to": timestamp+interval, "score": anomaly['ESD'] })

    result = { "name": "STL thermometr", "results": { "anomalies": formatted_anomalies } }
    return result


#for testing purposes
def generateRandomBaseline(series):
    baseline = []
    for element in series:
        baseline.append([element[0], element[1]-random.randint(0,9), element[1]+random.randint(0,9)] )
    return baseline

#for testing purposes
def generateRandomTrend(pdseries):
    #mean as trend
    mean = pdseries.mean()
    trend = []
    for element in pdseries.iteritems():
        print(int(element[0].timestamp() * 1000))
        trend.append([ int(element[0].timestamp() * 1000), mean] )
    return trend



#----------old-----------------
def detectAnomalies(series):
    ts = SeriesArrayToPandasSeries(series)
    stl = decompose(ts, period=336)  #una semana periodicidad
    det = thermometr.Thermometr(ts)
    result = det.detect()
    formatted_anomalies = []
    for anomaly in result:
        formatted_anomalies.append([ts.index[anomaly['index']].value // 10 ** 6, anomaly['ESD'] ])

    return formatted_anomalies

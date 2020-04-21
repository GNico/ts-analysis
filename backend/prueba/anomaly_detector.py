import pandas as pd
from .salib.model import series_analyzer

'''
Cada analisis devuelve el siguiente formato, donde cada key es opcional

analysis result format =
{   
    "name": "description"
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


def testAlgorithms(series):
    #print("JSON series:", series)
    pdseries = SeriesArrayToPandasSeries(series)
    analysis = []
    analyzer = series_analyzer.SeriesAnalyzer()
    salib_result = analyzer.analyze(pdseries)
    analysis.append(salib_result.output_format())
    analysis_results = {
        "series": series,
        "analysis": analysis
    }
    return analysis_results


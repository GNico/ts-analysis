from .salib.model import series_analyzer
from .salib.model import series

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


def testAlgorithms(arr_series):
    # print("JSON series:", series)
    target_series = series.Series.fromArray(arr_series)
    analyses = []
    analyzer = series_analyzer.SeriesAnalyzer()
    analyzer_result = analyzer.analyze(target_series)
    analyses.append(analyzer_result.output_format())
    result = {
        "series": arr_series,
        "analyses": analyses
    }
    return result

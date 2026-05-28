import numpy as np

def wmape(actual, forecast):
    actual = np.array(actual, dtype=float)
    forecast = np.array(forecast, dtype=float)
    denominator = np.abs(actual).sum()
    if denominator == 0:
        return 0.0
    return np.abs(actual - forecast).sum() / denominator * 100

def bias(actual, forecast):
    actual = np.array(actual, dtype=float)
    forecast = np.array(forecast, dtype=float)
    denominator = np.mean(actual)
    if denominator == 0:
        return 0.0
    return (np.mean(forecast) - np.mean(actual)) / denominator * 100

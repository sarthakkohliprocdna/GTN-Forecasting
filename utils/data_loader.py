import pandas as pd

def load_actuals(path="data/gtn_actuals.csv"):
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["month"])
    return df

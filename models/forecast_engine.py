import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from utils.metrics import wmape, bias

METRICS_TO_FORECAST = ["gross_sales", "rebates", "chargebacks", "medicaid", "medicare", "copay", "returns", "admin_fees", "other_deductions"]
DEDUCTIONS = ["rebates", "chargebacks", "medicaid", "medicare", "copay", "returns", "admin_fees", "other_deductions"]
BENCHMARK_MODELS = ["Naive Forecast", "Moving Average 3M", "Moving Average 6M", "Weighted Moving Average", "Holt-Winters", "Linear Regression", "Ridge Regression", "Lasso Regression", "Decision Tree", "Random Forest", "Gradient Boosting"]

def _time_features(n):
    x = np.arange(n)
    return pd.DataFrame({"t": x, "sin12": np.sin(2*np.pi*x/12), "cos12": np.cos(2*np.pi*x/12), "quarter_end": [1 if (i+1)%3==0 else 0 for i in x]})

def _predict_model(name, train_series, horizon=12):
    s = pd.Series(train_series).astype(float).reset_index(drop=True)
    n = len(s)
    if name == "Naive Forecast":
        return np.repeat(s.iloc[-1], horizon)
    if name == "Moving Average 3M":
        return np.repeat(s.tail(3).mean(), horizon)
    if name == "Moving Average 6M":
        return np.repeat(s.tail(6).mean(), horizon)
    if name == "Weighted Moving Average":
        weights = np.arange(1, min(6, n)+1)
        vals = s.tail(len(weights)).values
        return np.repeat(np.average(vals, weights=weights), horizon)
    if name == "Holt-Winters":
        slope = s.diff().tail(12).mean()
        seasonal = s.groupby(np.arange(n) % 12).mean()
        preds = []
        for h in range(1, horizon + 1):
            season_idx = (n + h - 1) % 12
            sf = seasonal.iloc[season_idx] / max(s.mean(), 1)
            preds.append(max((s.iloc[-1] + slope*h) * sf, 0))
        return np.array(preds)

    X = _time_features(n)
    Xf = _time_features(n + horizon).iloc[n:]
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Lasso Regression": Lasso(alpha=0.1),
        "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=80, max_depth=5, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }
    model = models.get(name, LinearRegression())
    model.fit(X, s.values)
    return np.maximum(model.predict(Xf), 0)

def benchmark_component(series):
    series = pd.Series(series).astype(float).reset_index(drop=True)
    train = series.iloc[:-12]
    test = series.iloc[-12:]
    rows = []
    for model_name in BENCHMARK_MODELS:
        pred = _predict_model(model_name, train, horizon=12)
        rows.append({"Model": model_name, "WMAPE": round(wmape(test.values, pred), 2), "Bias %": round(bias(test.values, pred), 2), "Stability": round(float(np.std(pred)), 2)})
    return pd.DataFrame(rows).sort_values("WMAPE").reset_index(drop=True)

def run_forecast(actuals_df, brand="All Brands", horizon=12):
    df = actuals_df.copy()
    df["month"] = pd.to_datetime(df["month"])
    if brand != "All Brands":
        df = df[df["brand"] == brand]
    monthly = df.groupby("month", as_index=False)[METRICS_TO_FORECAST].sum().sort_values("month")
    future_months = pd.date_range(monthly["month"].max() + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")
    forecast_payload = {"month": future_months}
    champion_rows = []
    model_details = {}
    for metric in METRICS_TO_FORECAST:
        benchmark = benchmark_component(monthly[metric])
        champion = benchmark.iloc[0]
        preds = _predict_model(champion["Model"], monthly[metric], horizon=horizon)
        forecast_payload[metric] = preds
        champion_rows.append({"GTN Component": metric, "Champion Model": champion["Model"], "WMAPE": champion["WMAPE"], "Bias %": champion["Bias %"], "Stability": champion["Stability"]})
        model_details[metric] = benchmark
    forecast_df = pd.DataFrame(forecast_payload)
    forecast_df["total_gtn"] = forecast_df[DEDUCTIONS].sum(axis=1)
    forecast_df["net_sales"] = forecast_df["gross_sales"] - forecast_df["total_gtn"]
    forecast_df["gtn_pct"] = forecast_df["total_gtn"] / forecast_df["gross_sales"]
    return {"forecast_df": forecast_df, "champion_df": pd.DataFrame(champion_rows), "model_details": model_details, "historical_monthly": monthly}

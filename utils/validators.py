REQUIRED_ACTUALS_COLUMNS = ["month", "brand", "gross_sales", "rebates", "chargebacks", "medicaid", "medicare", "copay", "returns", "admin_fees", "other_deductions"]

def validate_actuals(df):
    missing = [c for c in REQUIRED_ACTUALS_COLUMNS if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    try:
        import pandas as pd
        pd.to_datetime(df["month"])
    except Exception:
        return False, "Column 'month' must contain valid dates."
    for col in REQUIRED_ACTUALS_COLUMNS:
        if col in ["month", "brand"]:
            continue
        values = df[col].astype(float)
        if values.isna().any():
            return False, f"Column '{col}' contains blank or invalid values."
        if (values < 0).any():
            return False, f"Column '{col}' cannot contain negative values."
    return True, "Data validation passed."

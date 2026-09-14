"""
Step 1 — Load and clean the Volve production data.

Two sheets in the source file:
- Daily Production Data: well x day, includes pressures/temperatures/chokes
  and oil/gas/water/water-injection volumes. Has real gaps (not every well
  has downhole gauges, injectors don't produce oil, etc.) — that's expected,
  not a data quality problem to "fix".
- Monthly Production Data: well x month, aggregated volumes. The raw sheet
  has a units row (e.g. "Sm3") sitting inside the data as if it were a
  record — dropped here, and the volume columns are cast to numeric.
"""

from pathlib import Path

import pandas as pd

RAW_FILE = Path(__file__).resolve().parents[1] / "data" / "raw" / "Volve production data.xlsx"


def load_daily() -> pd.DataFrame:
    df = pd.read_excel(RAW_FILE, sheet_name="Daily Production Data")
    df["DATEPRD"] = pd.to_datetime(df["DATEPRD"])
    return df


def load_monthly() -> pd.DataFrame:
    df = pd.read_excel(RAW_FILE, sheet_name="Monthly Production Data")

    # First row is a units row (e.g. "Sm3" in the volume columns), not a well record.
    df = df.iloc[1:].reset_index(drop=True)

    numeric_cols = ["NPDCode", "Year", "Month", "On Stream", "Oil", "Gas", "Water", "GI", "WI"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Year"] = df["Year"].astype("Int64")
    df["Month"] = df["Month"].astype("Int64")
    return df


if __name__ == "__main__":
    daily = load_daily()
    monthly = load_monthly()

    print("Daily:", daily.shape, "|", daily["DATEPRD"].min().date(), "->", daily["DATEPRD"].max().date())
    print("Wells:", sorted(daily["NPD_WELL_BORE_NAME"].dropna().unique().tolist()))
    print("Monthly:", monthly.shape)
    print(monthly.dtypes)

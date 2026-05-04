"""
Fetch U.S. labor market data from the BLS Public Data API.

This script collects several monthly labor market indicators and saves them to:
data/bls_labor_data.csv

The project focuses on overall U.S. labor market conditions and healthcare employment.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests


SERIES: Dict[str, str] = {
    "LNS14000000": "Unemployment Rate",
    "CES0000000001": "Total Nonfarm Employment",
    "LNS11300000": "Labor Force Participation Rate",
    "CES0500000003": "Average Hourly Earnings",
    "CES0500000002": "Average Weekly Hours",
    "CES6562000001": "Healthcare Employment",
}

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
OUTPUT_PATH = Path("data/bls_labor_data.csv")


def fetch_bls_series(series_ids: List[str], start_year: int, end_year: int) -> pd.DataFrame:
    """Fetch multiple BLS time series from the public API."""
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
    }

    response = requests.post(BLS_API_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS API request failed: {data}")

    rows = []

    for series in data["Results"]["series"]:
        series_id = series["seriesID"]
        indicator = SERIES.get(series_id, series_id)

        for item in series["data"]:
            period = item.get("period", "")

            if not period.startswith("M"):
                continue

            month = int(period.replace("M", ""))
            year = int(item["year"])
            date = pd.Timestamp(year=year, month=month, day=1)

            rows.append(
                {
                    "date": date,
                    "year": year,
                    "month": month,
                    "series_id": series_id,
                    "indicator": indicator,
                    "value": float(item["value"]),
                    "latest": item.get("latest", False),
                }
            )

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No data returned from BLS API.")

    df = df.sort_values(["indicator", "date"]).reset_index(drop=True)
    df["month_to_month_change"] = df.groupby("indicator")["value"].diff()

    return df


def update_dataset() -> pd.DataFrame:
    """Fetch BLS data and save a clean CSV file."""
    current_year = datetime.now().year
    start_year = max(current_year - 6, 2019)
    end_year = current_year

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    new_data = fetch_bls_series(
        series_ids=list(SERIES.keys()),
        start_year=start_year,
        end_year=end_year,
    )

    if OUTPUT_PATH.exists():
        old_data = pd.read_csv(OUTPUT_PATH, parse_dates=["date"])
        combined = pd.concat([old_data, new_data], ignore_index=True)
        combined = combined.drop_duplicates(
            subset=["date", "series_id"],
            keep="last",
        )
    else:
        combined = new_data

    combined = combined.sort_values(["indicator", "date"]).reset_index(drop=True)
    combined["month_to_month_change"] = combined.groupby("indicator")["value"].diff()

    combined.to_csv(OUTPUT_PATH, index=False)
    return combined


if __name__ == "__main__":
    df = update_dataset()
    print(f"Saved {len(df):,} rows to {OUTPUT_PATH}")

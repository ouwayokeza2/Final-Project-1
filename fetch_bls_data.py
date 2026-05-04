import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

SERIES = {
    "UNRATE": {
        "indicator": "Unemployment Rate",
        "unit": "%"
    },
    "PAYEMS": {
        "indicator": "Total Nonfarm Employment",
        "unit": "thousands of jobs"
    },
    "CES6562000001": {
        "indicator": "Healthcare Employment",
        "unit": "thousands of jobs"
    },
    "CIVPART": {
        "indicator": "Labor Force Participation Rate",
        "unit": "%"
    },
    "CES0500000003": {
        "indicator": "Average Hourly Earnings",
        "unit": "dollars"
    },
    "CES0500000002": {
        "indicator": "Average Weekly Hours",
        "unit": "hours"
    }
}

START_YEAR = "2020"
END_YEAR = str(datetime.now().year)
DATA_PATH = Path("data/bls_labor_data.csv")


def fetch_bls_data():
    payload = {
        "seriesid": list(SERIES.keys()),
        "startyear": START_YEAR,
        "endyear": END_YEAR
    }

    response = requests.post(BLS_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    rows = []

    for series in data.get("Results", {}).get("series", []):
        series_id = series["seriesID"]
        meta = SERIES.get(series_id, {})

        for item in series.get("data", []):
            period = item.get("period", "")

            if not period.startswith("M"):
                continue

            year = int(item["year"])
            month = int(period.replace("M", ""))
            date = pd.Timestamp(year=year, month=month, day=1)

            rows.append({
                "series_id": series_id,
                "indicator": meta.get("indicator", series_id),
                "date": date,
                "value": float(item["value"]),
                "unit": meta.get("unit", "")
            })

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No data was returned from the BLS API.")

    df = df.drop_duplicates(subset=["series_id", "date"])
    df = df.sort_values(["indicator", "date"])

    DATA_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print(f"Saved {len(df)} rows to {DATA_PATH}")


if __name__ == "__main__":
    fetch_bls_data()

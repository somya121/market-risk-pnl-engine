from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT/"market-risk-pnl-engine" / "data" / "raw"


TREASURY_SERIES = {
    "US2Y": "DGS2",
    "US5Y": "DGS5",
    "US10Y": "DGS10",
}


def download_treasury_data(
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
) -> None:

    # Convert date strings to datetime objects
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    for name, series_id in TREASURY_SERIES.items():

        print(f"\nDownloading {name} ({series_id})...")

        url = (
            "https://fred.stlouisfed.org/graph/"
            f"fredgraph.csv?id={series_id}"
        )

        data = pd.read_csv(url)

        # Reset index if DATE is the index
        if data.index.name == "DATE" or "DATE" in data.index.names:
            data = data.reset_index()

        # Handle both uppercase DATE and other possible column names
        date_col = None
        if "DATE" in data.columns:
            date_col = "DATE"
        elif "date" in data.columns:
            date_col = "date"
        else:
            # Use the first column as date if it's a datetime-like column
            date_col = data.columns[0]

        data[date_col] = pd.to_datetime(data[date_col])

        data = data[
            (data[date_col] >= start_dt)
            & (data[date_col] <= end_dt)
        ].copy()

        data = data.rename(
            columns={
                date_col: "Date",
                series_id: "Yield"
            }
        )

        data["Yield"] = pd.to_numeric(
            data["Yield"],
            errors="coerce"
        )

        data = data.dropna(
            subset=["Yield"]
        )

        data = data.set_index("Date")

        output_file = (
            RAW_DATA_DIR / f"{name}.csv"
        )

        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        data.to_csv(output_file)

        print(f"Saved: {output_file}")
        print(f"Rows: {len(data)}")


if __name__ == "__main__":
    download_treasury_data()
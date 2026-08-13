from pathlib import Path
import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


TICKERS = [
    "AAPL",
    "SPY",
    "MSFT",
    "EURUSD=X",
    "^VIX",
]


def download_market_data(
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
) -> None:

    print("Downloading market data...")

    data = yf.download(
        TICKERS,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        threads=True,
    )

    if data.empty:
        raise ValueError("No market data was downloaded.")

    output_file = RAW_DATA_DIR / "market_data_raw.csv"

    data.to_csv(output_file)

    print(f"Saved market data to: {output_file}")
    print(f"Rows: {len(data)}")


if __name__ == "__main__":
    download_market_data()
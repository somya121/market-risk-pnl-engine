from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


MARKET_DATA = {
    "AAPL": "AAPL",
    "SPY": "SPY",
    "MSFT": "MSFT",
    "EURUSD": "EURUSD=X",
    "VIX": "^VIX",
}


def download_ticker(
    name: str,
    ticker: str,
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
) -> None:

    print(f"\nDownloading {name} ({ticker})...")

    data = yf.Ticker(ticker).history(
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=True,
    )

    if data.empty:
        raise ValueError(
            f"No data returned for {name} ({ticker})"
        )

    data = data[
        ["Open", "High", "Low", "Close", "Volume"]
    ].copy()

    data.index = pd.to_datetime(data.index)

    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    data.index.name = "Date"

    output_file = RAW_DATA_DIR / f"{name}.csv"

    data.to_csv(output_file)

    print(f"Saved: {output_file}")
    print(f"Rows: {len(data)}")
    print(f"Start: {data.index.min().date()}")
    print(f"End:   {data.index.max().date()}")


def download_all_market_data() -> None:

    failures = []

    for name, ticker in MARKET_DATA.items():

        try:
            download_ticker(name, ticker)

        except Exception as exc:

            print(
                f"FAILED: {name} ({ticker})"
            )

            print(f"Reason: {exc}")

            failures.append(name)

    print("\n" + "=" * 60)
    print("MARKET DATA DOWNLOAD SUMMARY")
    print("=" * 60)

    if failures:
        print("Failed datasets:")
        for name in failures:
            print(f"  - {name}")
    else:
        print("All market datasets downloaded successfully.")


if __name__ == "__main__":
    download_all_market_data()
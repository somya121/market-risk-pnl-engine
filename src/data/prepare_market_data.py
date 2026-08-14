from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_equity_data(
    name: str,
) -> pd.Series:

    file_path = RAW_DATA_DIR / f"{name}.csv"

    data = pd.read_csv(
        file_path,
        parse_dates=["Date"],
        index_col="Date",
    )

    series = data["Close"].rename(name)

    return series


def load_treasury_data(
    name: str,
) -> pd.Series:

    file_path = RAW_DATA_DIR / f"{name}.csv"

    data = pd.read_csv(
        file_path,
        parse_dates=["Date"],
        index_col="Date",
    )

    series = data["Yield"].rename(name)

    return series


def build_market_factor_dataset():

    print("Loading market factors...")

    factors = pd.concat(
        [
            load_equity_data("AAPL"),
            load_equity_data("SPY"),
            load_equity_data("MSFT"),
            load_equity_data("EURUSD"),
            load_equity_data("VIX"),
            load_treasury_data("US2Y"),
            load_treasury_data("US5Y"),
            load_treasury_data("US10Y"),
        ],
        axis=1,
        join="inner"
    )

    factors = factors.sort_index()
    factors = factors.drop_duplicates(keep="first")
    factors.index.name = "Date"

    output_file = (
        PROCESSED_DATA_DIR
        / "market_factors.parquet"
    )

    factors.to_parquet(output_file)

    print("\nMarket factor dataset created.")

    print(f"Rows: {len(factors)}")
    print(f"Columns: {len(factors.columns)}")

    print("\nColumns:")
    print(factors.columns.tolist())

    print("\nMissing values:")
    print(factors.isna().sum())

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    build_market_factor_dataset()
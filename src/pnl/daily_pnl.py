import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pricing.valuation import value_portfolio

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def load_market_dates():

    market_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "market_factors.parquet"
    )

    market_data = pd.read_parquet(
        market_file
    )

    return market_data.index


def calculate_daily_portfolio_values():

    dates = load_market_dates()

    results = []

    print(
        f"Calculating portfolio valuation "
        f"for {len(dates)} dates..."
    )

    for date in dates:

        valuation = value_portfolio(
            valuation_date=date
        )

        total_value = (
            valuation["market_value"]
            .sum()
        )

        results.append(
            {
                "date": date,
                "portfolio_value": total_value,
            }
        )

    result = pd.DataFrame(
        results
    )

    result["date"] = pd.to_datetime(
        result["date"]
    )

    result = result.sort_values(
        "date"
    )

    result["daily_pnl"] = (
        result["portfolio_value"]
        .diff()
    )

    return result


def save_daily_pnl():

    result = (
        calculate_daily_portfolio_values()
    )

    output_file = (
        REPORT_DIR
        / "daily_pnl.csv"
    )

    result.to_csv(
        output_file,
        index=False
    )

    print(
        "\nDaily P&L calculated."
    )

    print(
        result.head(10)
    )

    print(
        f"\nSaved to: {output_file}"
    )


if __name__ == "__main__":

    save_daily_pnl()
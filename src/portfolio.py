from pathlib import Path

import yaml
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PORTFOLIO_FILE = (
    PROJECT_ROOT
    / "config"
    / "portfolio.yaml"
)


def load_portfolio() -> pd.DataFrame:

    with open(
        PORTFOLIO_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    trades = config["trades"]

    portfolio = pd.DataFrame(trades)

    return portfolio

def validate_portfolio(
    portfolio: pd.DataFrame,
) -> None:

    required_columns = [
        "trade_id",
        "instrument_type",
        "underlying",
        "quantity",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in portfolio.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    if portfolio["trade_id"].duplicated().any():
        raise ValueError(
            "Duplicate trade IDs found."
        )

    if portfolio["quantity"].isna().any():
        raise ValueError(
            "Missing trade quantities found."
        )

    if (portfolio["quantity"] == 0).any():
        raise ValueError(
            "Zero quantity trade found."
        )

    print("Portfolio validation: PASS")


if __name__ == "__main__":

    portfolio = load_portfolio()

    validate_portfolio(portfolio)

    print(
        portfolio.to_string(
            index=False
        )
    )
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.risk_analytics import (
    historical_var,
    historical_expected_shortfall,
    rolling_var,
)

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def generate_risk_metrics():

    daily_pnl_file = (
        REPORT_DIR
        / "daily_pnl.csv"
    )

    daily_pnl = pd.read_csv(
        daily_pnl_file,
        parse_dates=["date"],
    )

    var_99 = historical_var(
        daily_pnl["daily_pnl"],
        confidence=0.99,
    )

    es_99 = historical_expected_shortfall(
        daily_pnl["daily_pnl"],
        confidence=0.99,
    )

    daily_pnl[
        "rolling_var_99"
    ] = rolling_var(
        daily_pnl["daily_pnl"],
        window=250,
        confidence=0.99,
    )

    daily_pnl.to_csv(
        daily_pnl_file,
        index=False,
    )

    metrics = pd.DataFrame(
        {
            "metric": [
                "Historical VaR 99%",
                "Expected Shortfall 99%",
                "Worst Daily P&L",
                "Average Daily P&L",
                "Daily P&L Volatility",
            ],
            "value": [
                var_99,
                es_99,
                daily_pnl["daily_pnl"].min(),
                daily_pnl["daily_pnl"].mean(),
                daily_pnl["daily_pnl"].std(),
            ],
        }
    )

    output_file = (
        REPORT_DIR
        / "risk_metrics.csv"
    )

    metrics.to_csv(
        output_file,
        index=False,
    )

    print(metrics)

    print(
        f"\nSaved to: {output_file}"
    )

    return metrics


if __name__ == "__main__":
    generate_risk_metrics()
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.risk.limit_monitor import (
    evaluate_risk_limits,
)

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)


def generate_risk_limit_report():

    risk_metrics = pd.read_csv(
        REPORT_DIR
        / "risk_metrics.csv"
    )

    stress_results = pd.read_csv(
        REPORT_DIR
        / "stress_results.csv"
    )

    daily_pnl = pd.read_csv(
        REPORT_DIR
        / "daily_pnl.csv"
    )

    var_99 = float(
        risk_metrics.loc[
            risk_metrics["metric"]
            == "Historical VaR 99%",
            "value",
        ].iloc[0]
    )

    es_99 = float(
        risk_metrics.loc[
            risk_metrics["metric"]
            == "Expected Shortfall 99%",
            "value",
        ].iloc[0]
    )

    daily_loss = (
        daily_pnl["daily_pnl"].min()
    )

    stress_loss = (
        stress_results["stress_pnl"].min()
    )

    results = evaluate_risk_limits(
        var_99=var_99,
        expected_shortfall_99=es_99,
        daily_loss=daily_loss,
        stress_loss=stress_loss,
    )

    output_file = (
        REPORT_DIR
        / "risk_limit_results.csv"
    )

    results.to_csv(
        output_file,
        index=False,
    )

    print(results)

    print(
        f"\nSaved to: {output_file}"
    )

    return results


if __name__ == "__main__":
    generate_risk_limit_report()
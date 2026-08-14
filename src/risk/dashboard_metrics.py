from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


def build_dashboard_metrics():

    risk_metrics = pd.read_csv(
        PROJECT_ROOT
        / "reports"
        / "risk_metrics.csv"
    )

    stress = pd.read_csv(
        PROJECT_ROOT
        / "reports"
        / "stress_results.csv"
    )

    limits = pd.read_csv(
        PROJECT_ROOT
        / "reports"
        / "risk_limit_results.csv"
    )

    daily_pnl = pd.read_csv(
        PROJECT_ROOT
        / "reports"
        / "daily_pnl.csv"
    )

    return {
        "var_99": float(
            risk_metrics.loc[
                risk_metrics["metric"]
                == "Historical VaR 99%",
                "value",
            ].iloc[0]
        ),
        "es_99": float(
            risk_metrics.loc[
                risk_metrics["metric"]
                == "Expected Shortfall 99%",
                "value",
            ].iloc[0]
        ),
        "worst_daily_pnl": float(
            daily_pnl[
                "daily_pnl"
            ].min()
        ),
        "worst_stress_pnl": float(
            stress[
                "stress_pnl"
            ].min()
        ),
        "breaches": int(
            (
                limits["status"]
                == "BREACH"
            ).sum()
        ),
        "warnings": int(
            (
                limits["status"]
                == "WARNING"
            ).sum()
        ),
    }
from pathlib import Path

import pandas as pd

from src.pricing.valuation import (
    value_portfolio,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def generate_sensitivity_report():

    portfolio = value_portfolio()

    total_market_value = (
        portfolio["market_value"]
        .sum()
    )

    total_delta = (
        portfolio["delta"]
        .sum()
    )

    total_gamma = (
        portfolio["gamma"]
        .sum()
    )

    total_vega = (
        portfolio["vega"]
        .sum()
    )

    total_rho = (
        portfolio["rho"]
        .sum()
    )

    total_theta = (
        portfolio["theta"]
        .sum()
    )

    total_ir_dv01 = (
        portfolio["ir_dv01"]
        .sum()
    )
    total_vega_1pt = (
        total_vega * 0.01
    )

    summary = pd.DataFrame(
        {
            "metric": [
                "Total Market Value",
                "Delta",
                "Gamma",
                "Vega",
                "Vega per 1 Vol Point",
                "Rho",
                "Theta",
                "IR DV01",
            ],
            "value": [
                total_market_value,
                total_delta,
                total_gamma,
                total_vega,
                total_vega_1pt,
                total_rho,
                total_theta,
                total_ir_dv01,
            ],
        }
    )

    print("\nPORTFOLIO RISK SENSITIVITIES")
    print("=" * 50)

    print(
        summary.to_string(
            index=False
        )
    )

    output_file = (
        REPORT_DIR
        / "portfolio_sensitivities.csv"
    )

    summary.to_csv(
        output_file,
        index=False,
    )

    print(
        f"\nSaved to: {output_file}"
    )


if __name__ == "__main__":

    generate_sensitivity_report()
import sys
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pricing.valuation import value_portfolio


def load_stress_scenarios():
    scenario_file = (
        PROJECT_ROOT
        / "config"
        / "stress_scenarios.yaml"
    )

    with open(
        scenario_file,
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    return config["scenarios"]


def run_stress_scenarios():

    base_portfolio = value_portfolio()

    base_value = (
        base_portfolio["market_value"]
        .sum()
    )

    results = []

    for scenario in load_stress_scenarios():

        spot_shocks = scenario.get(
            "spot_shocks",
            {},
        )

        volatility_shock = scenario.get(
            "volatility_shock",
            0.0,
        )

        rate_shock = scenario.get(
            "rate_shock",
            0.0,
        )

        scenario_pnl = 0.0

        for _, trade in base_portfolio.iterrows():

            underlying = trade["underlying"]

            spot = trade["spot"]

            spot_change = (
                spot
                * spot_shocks.get(
                    underlying,
                    0.0,
                )
            )

            delta = trade["delta"]
            gamma = trade["gamma"]
            vega = trade["vega"]
            ir_dv01 = trade["ir_dv01"]

            scenario_pnl += (
                delta * spot_change
                + 0.5
                * gamma
                * spot_change**2
                + vega
                * volatility_shock
                - ir_dv01
                * rate_shock
                / 0.0001
            )

        results.append(
            {
                "scenario": scenario["name"],
                "description": scenario["description"],
                "base_portfolio_value": base_value,
                "stress_pnl": scenario_pnl,
                "stressed_value":
                    base_value + scenario_pnl,
            }
        )

    return pd.DataFrame(results)


if __name__ == "__main__":

    result = run_stress_scenarios()

    report_dir = (
        PROJECT_ROOT / "reports"
    )

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        report_dir
        / "stress_results.csv"
    )

    result.to_csv(
        output_file,
        index=False,
    )

    print(result)
    print(
        f"\nSaved to: {output_file}"
    )
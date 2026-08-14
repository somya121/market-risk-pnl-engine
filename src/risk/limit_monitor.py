from pathlib import Path

import yaml
import pandas as pd


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


def load_limits():

    file_path = (
        PROJECT_ROOT
        / "config"
        / "risk_limits.yaml"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(file)["limits"]


def evaluate_limit(
    metric,
    value,
):

    limits = load_limits()[metric]

    if metric in {
        "daily_loss",
        "stress_loss",
    }:

        if value <= limits["breach"]:
            status = "BREACH"

        elif value <= limits["warning"]:
            status = "WARNING"

        else:
            status = "PASS"

    else:

        if value >= limits["breach"]:
            status = "BREACH"

        elif value >= limits["warning"]:
            status = "WARNING"

        else:
            status = "PASS"

    return {
        "metric": metric,
        "value": value,
        "warning_limit": limits["warning"],
        "breach_limit": limits["breach"],
        "status": status,
    }


def evaluate_risk_limits(
    var_99,
    expected_shortfall_99,
    daily_loss,
    stress_loss,
):

    values = {
        "var_99": var_99,
        "expected_shortfall_99":
            expected_shortfall_99,
        "daily_loss": daily_loss,
        "stress_loss": stress_loss,
    }

    return pd.DataFrame(
        [
            evaluate_limit(
                metric,
                value,
            )
            for metric, value
            in values.items()
        ]
    )
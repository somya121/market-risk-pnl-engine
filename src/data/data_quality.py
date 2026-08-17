from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_factors.parquet"
)

REPORT_DIR = PROJECT_ROOT / "reports"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


EXPECTED_FACTORS = {
    "AAPL",
    "SPY",
    "MSFT",
    "EURUSD",
    "VIX",
    "US2Y",
    "US5Y",
    "US10Y",
}


PRICE_FACTORS = {
    "AAPL",
    "SPY",
    "MSFT",
    "EURUSD",
}


RATE_FACTORS = {
    "US2Y",
    "US5Y",
    "US10Y",
}


def generate_quality_report():

    data = pd.read_parquet(
        INPUT_FILE
    )

    issues = []

    # --------------------------------------------------
    # Dataset-level checks
    # --------------------------------------------------

    if data.empty:
        issues.append(
            "Market data dataset is empty."
        )

    missing_factors = (
        EXPECTED_FACTORS
        - set(data.columns)
    )

    if missing_factors:
        issues.append(
            "Missing expected factors: "
            + ", ".join(
                sorted(missing_factors)
            )
        )

    if not isinstance(
        data.index,
        pd.DatetimeIndex
    ):
        issues.append(
            "Market data index is not a DatetimeIndex."
        )
    else:

        if data.index.duplicated().any():
            issues.append(
                "Duplicate dates found."
            )

        if not data.index.is_monotonic_increasing:
            issues.append(
                "Dates are not sorted in ascending order."
            )

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    if data.isna().any().any():
        issues.append(
            "Missing values found in market data."
        )

    # --------------------------------------------------
    # Numeric validation
    # --------------------------------------------------

    for column in data.columns:

        if not pd.api.types.is_numeric_dtype(
            data[column]
        ):
            issues.append(
                f"{column}: non-numeric data found."
            )

    # --------------------------------------------------
    # Price validation
    # --------------------------------------------------

    for column in PRICE_FACTORS:

        if column in data.columns:

            if (
                data[column] <= 0
            ).any():

                issues.append(
                    f"{column}: "
                    "non-positive value found."
                )

    # --------------------------------------------------
    # VIX validation
    # --------------------------------------------------

    if "VIX" in data.columns:

        if (
            data["VIX"] < 0
        ).any():

            issues.append(
                "VIX: negative value found."
            )

    # --------------------------------------------------
    # Interest-rate validation
    # --------------------------------------------------

    for column in RATE_FACTORS:

        if column in data.columns:

            if (
                data[column].isna().any()
            ):

                issues.append(
                    f"{column}: missing rate values."
                )

    # --------------------------------------------------
    # Build report
    # --------------------------------------------------

    report = pd.DataFrame(
        {
            "factor": data.columns,

            "observations": [
                data[column].count()
                for column in data.columns
            ],

            "missing_values": [
                data[column].isna().sum()
                for column in data.columns
            ],

            "missing_pct": [
                data[column].isna().mean() * 100
                for column in data.columns
            ],

            "min": [
                data[column].min()
                for column in data.columns
            ],

            "max": [
                data[column].max()
                for column in data.columns
            ],
        }
    )

    overall_status = (
        "PASS"
        if not issues
        else "REVIEW"
    )

    report["status"] = overall_status

    output_file = (
        REPORT_DIR
        / "market_data_quality.csv"
    )

    report.to_csv(
        output_file,
        index=False
    )

    print(report)

    print(
        f"\nOverall status:"
    )

    print(
        overall_status
    )

    if issues:

        print(
            "\nIssues:"
        )

        for issue in issues:

            print(
                f"- {issue}"
            )

    print(
        f"\nSaved report to: "
        f"{output_file}"
    )

    return report, overall_status


if __name__ == "__main__":

    generate_quality_report()
from pathlib import Path
import sys

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))

from src.pricing.valuation import (
    value_portfolio,
)

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def generate_risk_report():

    portfolio = value_portfolio()

    report_file = (
        REPORT_DIR
        / "portfolio_risk_report.csv"
    )

    portfolio.to_csv(
        report_file,
        index=False,
    )

    print(
        "\nPortfolio Risk Report"
    )

    print(
        "=" * 70
    )

    print(
        portfolio.to_string(
            index=False
        )
    )

    print(
        f"\nSaved to: {report_file}"
    )


if __name__ == "__main__":

    generate_risk_report()
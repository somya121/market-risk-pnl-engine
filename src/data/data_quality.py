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


def generate_quality_report():

    data = pd.read_parquet(
        INPUT_FILE
    )

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

    report["status"] = report[
        "missing_values"
    ].apply(
        lambda x: (
            "PASS"
            if x == 0
            else "REVIEW"
        )
    )

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
        f"\nSaved report to: {output_file}"
    )


if __name__ == "__main__":
    generate_quality_report()
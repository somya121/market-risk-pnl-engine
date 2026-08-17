import pandas as pd

from src.data.data_quality import (
    generate_quality_report,
)


def test_quality_report_runs():

    report, status = (
        generate_quality_report()
    )

    assert not report.empty
    assert status == "PASS"


def test_quality_report_contains_expected_factors():

    report, status = (
        generate_quality_report()
    )

    expected_factors = {
        "AAPL",
        "SPY",
        "MSFT",
        "EURUSD",
        "VIX",
        "US2Y",
        "US5Y",
        "US10Y",
    }

    assert set(report["factor"]) == (
        expected_factors
    )


def test_quality_report_has_no_missing_values():

    report, status = (
        generate_quality_report()
    )

    assert (
        report["missing_values"]
        .sum()
        == 0
    )

    assert status == "PASS"
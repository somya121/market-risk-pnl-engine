from src.risk.limit_monitor import (
    evaluate_limit,
)


def test_limit_pass():

    result = evaluate_limit(
        "var_99",
        50000,
    )

    assert result["status"] == "PASS"


def test_limit_breach():

    result = evaluate_limit(
        "var_99",
        150000,
    )

    assert result["status"] == "BREACH"
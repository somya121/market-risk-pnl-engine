from src.risk.stress_testing import (
    run_stress_scenarios,
)


def test_stress_scenarios():

    result = (
        run_stress_scenarios()
    )

    assert not result.empty

    assert {
        "scenario",
        "stress_pnl",
        "stressed_value",
    }.issubset(
        result.columns
    )
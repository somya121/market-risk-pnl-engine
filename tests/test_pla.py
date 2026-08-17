import math

import pandas as pd

from src.risk.pla import calculate_pla_statistics


def test_pla_statistics_reconcile():

    attribution = pd.DataFrame(
        {
            "actual_pnl": [
                100.0,
                -200.0,
                50.0,
            ],
            "explained_pnl": [
                90.0,
                -180.0,
                40.0,
            ],
            "unexplained_pnl": [
                10.0,
                -20.0,
                10.0,
            ],
        }
    )

    stats = calculate_pla_statistics(
        attribution
    )

    assert math.isclose(
        stats["reconciliation_error"],
        0.0,
        abs_tol=1e-10,
    )


def test_unexplained_ratio_is_non_negative():

    attribution = pd.DataFrame(
        {
            "actual_pnl": [100.0, -200.0],
            "explained_pnl": [90.0, -180.0],
            "unexplained_pnl": [10.0, -20.0],
        }
    )

    stats = calculate_pla_statistics(
        attribution
    )

    assert stats["unexplained_ratio"] >= 0
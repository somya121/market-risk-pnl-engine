import numpy as np

from src.risk_analytics import (
    historical_var,
    historical_expected_shortfall,
)


def test_historical_var():

    pnl = np.array(
        [-100, -50, 0, 50, 100]
    )

    var = historical_var(
        pnl,
        confidence=0.80,
    )

    assert var >= 0


def test_expected_shortfall():

    pnl = np.array(
        [-100, -50, 0, 50, 100]
    )

    es = historical_expected_shortfall(
        pnl,
        confidence=0.80,
    )

    assert es >= 0
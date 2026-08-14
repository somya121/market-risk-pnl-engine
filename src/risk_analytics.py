import numpy as np
import pandas as pd


def historical_var(pnl, confidence=0.99):
    pnl = pd.Series(pnl).dropna()

    return -np.quantile(
        pnl,
        1 - confidence
    )


def historical_expected_shortfall(pnl, confidence=0.99):
    pnl = pd.Series(pnl).dropna()

    var_threshold = np.quantile(
        pnl,
        1 - confidence
    )

    tail_losses = pnl[pnl <= var_threshold]

    return -tail_losses.mean()


def rolling_var(pnl, window=250, confidence=0.99):
    pnl = pd.Series(pnl)

    return (
        pnl
        .rolling(window)
        .quantile(1 - confidence)
        .mul(-1)
    )
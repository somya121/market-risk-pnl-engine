import pandas as pd


def estimate_option_pnl(
    delta: float,
    gamma: float,
    vega: float,
    spot_change: float,
    volatility_change: float,
):
    return (
        delta * spot_change
        + 0.5
        * gamma
        * spot_change**2
        + vega
        * volatility_change
    )


def estimate_portfolio_shock_pnl(
    portfolio: pd.DataFrame,
    spot_changes: dict,
    volatility_change: float = 0.0,
):

    results = []

    for _, trade in portfolio.iterrows():

        underlying = trade[
            "underlying"
        ]

        spot_change = spot_changes.get(
            underlying,
            0.0,
        )

        pnl = (
            trade["delta"]
            * spot_change
            + 0.5
            * trade["gamma"]
            * spot_change**2
            + trade["vega"]
            * volatility_change
        )

        results.append(
            {
                "trade_id": trade[
                    "trade_id"
                ],
                "underlying": underlying,
                "estimated_pnl": pnl,
            }
        )

    return pd.DataFrame(
        results
    )
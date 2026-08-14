import pandas as pd


def revalue_forward_history(
    market_data,
    strike,
    notional,
    maturity_years
):
    results = []

    for _, row in market_data.iterrows():

        value = (
            row["spot"] -
            strike
        ) * notional

        results.append({
            "date": row["date"],
            "portfolio_value": value
        })

    return pd.DataFrame(results)
from pathlib import Path

import pandas as pd

from src.pricing.valuation import value_portfolio


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "reports"


def load_market_data():
    market_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "market_factors.parquet"
    )

    return pd.read_parquet(market_file)


def calculate_trade_attribution(
    previous_valuation,
    current_valuation,
    previous_date,
    current_date,
):
    """
    Calculate sensitivity-based P&L attribution
    between two consecutive valuation dates.
    """

    rows = []

    previous = previous_valuation.set_index("trade_id")
    current = current_valuation.set_index("trade_id")

    common_trades = previous.index.intersection(
        current.index
    )

    dt = (
        pd.Timestamp(current_date)
        - pd.Timestamp(previous_date)
    ).days / 365.0

    for trade_id in common_trades:

        prev = previous.loc[trade_id]
        curr = current.loc[trade_id]

        instrument_type = curr["instrument_type"]

        actual_pnl = (
            curr["market_value"]
            - prev["market_value"]
        )

        delta_pnl = 0.0
        gamma_pnl = 0.0
        vega_pnl = 0.0
        rho_pnl = 0.0
        theta_pnl = 0.0
        ir_pnl = 0.0

        spot_change = (
            curr["spot"]
            - prev["spot"]
        )

        rate_change = (
            curr["rate"]
            - prev["rate"]
        )

        if instrument_type == "EQUITY":

            delta_pnl = (
                prev["delta"]
                * spot_change
            )

        elif instrument_type in (
            "EUROPEAN_CALL",
            "EUROPEAN_PUT",
        ):

            delta_pnl = (
                prev["delta"]
                * spot_change
            )

            gamma_pnl = (
                0.5
                * prev["gamma"]
                * spot_change ** 2
            )

            # Volatility is currently static in
            # the portfolio configuration.
            vega_pnl = 0.0

            rho_pnl = (
                prev["rho"]
                * rate_change
            )

            theta_pnl = (
                prev["theta"]
                * dt
            )

        elif instrument_type == "BOND":

            rate_change_bp = (
                rate_change * 10000.0
            )

            ir_pnl = (
                -prev["ir_dv01"]
                * rate_change_bp
            )

        elif instrument_type == "FX_FORWARD":

            delta_pnl = (
                prev["delta"]
                * spot_change
            )

        explained_pnl = (
            delta_pnl
            + gamma_pnl
            + vega_pnl
            + rho_pnl
            + theta_pnl
            + ir_pnl
        )

        unexplained_pnl = (
            actual_pnl
            - explained_pnl
        )

        rows.append(
            {
                "date": current_date,
                "trade_id": trade_id,
                "instrument_type": instrument_type,
                "actual_pnl": actual_pnl,
                "delta_pnl": delta_pnl,
                "gamma_pnl": gamma_pnl,
                "vega_pnl": vega_pnl,
                "rho_pnl": rho_pnl,
                "theta_pnl": theta_pnl,
                "ir_pnl": ir_pnl,
                "explained_pnl": explained_pnl,
                "unexplained_pnl": unexplained_pnl,
            }
        )

    return pd.DataFrame(rows)


def calculate_pnl_attribution(
    daily_pnl=None,
):
    """
    Calculate historical P&L attribution using
    previous-day portfolio sensitivities and
    market-factor movements.
    """

    market_data = load_market_data()

    dates = pd.to_datetime(
        market_data.index
    ).sort_values()

    attribution_results = []

    print(
        f"Calculating P&L attribution "
        f"for {len(dates) - 1} periods..."
    )

    for i in range(1, len(dates)):

        previous_date = dates[i - 1]
        current_date = dates[i]

        previous_valuation = (
            value_portfolio(
                valuation_date=previous_date
            )
        )

        current_valuation = (
            value_portfolio(
                valuation_date=current_date
            )
        )

        daily_attribution = (
            calculate_trade_attribution(
                previous_valuation=previous_valuation,
                current_valuation=current_valuation,
                previous_date=previous_date,
                current_date=current_date,
            )
        )

        if not daily_attribution.empty:

            daily_summary = {
                "date": current_date,
                "actual_pnl": (
                    daily_attribution[
                        "actual_pnl"
                    ].sum()
                ),
                "delta_pnl": (
                    daily_attribution[
                        "delta_pnl"
                    ].sum()
                ),
                "gamma_pnl": (
                    daily_attribution[
                        "gamma_pnl"
                    ].sum()
                ),
                "vega_pnl": (
                    daily_attribution[
                        "vega_pnl"
                    ].sum()
                ),
                "rho_pnl": (
                    daily_attribution[
                        "rho_pnl"
                    ].sum()
                ),
                "theta_pnl": (
                    daily_attribution[
                        "theta_pnl"
                    ].sum()
                ),
                "ir_pnl": (
                    daily_attribution[
                        "ir_pnl"
                    ].sum()
                ),
                "explained_pnl": (
                    daily_attribution[
                        "explained_pnl"
                    ].sum()
                ),
                "unexplained_pnl": (
                    daily_attribution[
                        "unexplained_pnl"
                    ].sum()
                ),
            }

            attribution_results.append(
                daily_summary
            )

    result = pd.DataFrame(
        attribution_results
    )

    return result


def calculate_pla_statistics(
    attribution,
):
    """
    Calculate summary statistics for P&L attribution.
    """

    result = attribution.dropna(
        subset=["actual_pnl"]
    ).copy()

    total_abs_pnl = (
        result["actual_pnl"]
        .abs()
        .sum()
    )

    total_abs_explained = (
        result["explained_pnl"]
        .abs()
        .sum()
    )

    total_abs_unexplained = (
        result["unexplained_pnl"]
        .abs()
        .sum()
    )

    unexplained_ratio = (
        total_abs_unexplained
        / total_abs_pnl
        if total_abs_pnl != 0
        else 0.0
    )

    explained_ratio = (
        total_abs_explained
        / total_abs_pnl
        if total_abs_pnl != 0
        else 0.0
    )

    return {
        "total_abs_pnl": total_abs_pnl,
        "total_abs_explained_pnl": total_abs_explained,
        "total_abs_unexplained_pnl": total_abs_unexplained,
        "explained_ratio": explained_ratio,
        "unexplained_ratio": unexplained_ratio,
    }
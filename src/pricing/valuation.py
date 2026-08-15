import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

# Add project root to path for imports
project_root_path = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root_path))

from src.pricing.black_scholes import (
    call_price,
    put_price,
)
from src.pricing.greeks import (
    option_greeks,
)

from src.fx_forward import (
    forward_value,
)

def load_market_data():

    from pathlib import Path

    project_root = Path(
        __file__
    ).resolve().parents[2]

    file_path = (
        project_root
        / "data"
        / "processed"
        / "market_factors.parquet"
    )

    return pd.read_parquet(
        file_path
    )


def load_portfolio():

    from pathlib import Path

    project_root = Path(
        __file__
    ).resolve().parents[2]

    file_path = (
        project_root
        / "config"
        / "portfolio.yaml"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    return pd.DataFrame(
        config["trades"]
    )


def get_valuation_date(
    market_data: pd.DataFrame,
):

    return market_data.index.max()


def get_spot(
    market_data: pd.DataFrame,
    underlying: str,
    valuation_date,
):

    return float(
        market_data.loc[
            valuation_date,
            underlying,
        ]
    )


def get_risk_free_rate(
    market_data: pd.DataFrame,
    valuation_date,
):

    return float(
        market_data.loc[
            valuation_date,
            "US10Y",
        ]
    ) / 100.0


def year_fraction(
    valuation_date,
    maturity_date: str,
):

    maturity = datetime.strptime(
        maturity_date,
        "%Y-%m-%d",
    ).date()

    valuation = valuation_date.date()

    days = (
        maturity - valuation
    ).days

    return days / 365.0
def value_option(
    option_type: str,
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float,
    quantity: float,
):

    if option_type == "CALL":

        unit_price = call_price(
            spot=spot,
            strike=strike,
            rate=rate,
            volatility=volatility,
            time_to_maturity=time_to_maturity,
            dividend_yield=dividend_yield,
        )

    elif option_type == "PUT":

        unit_price = put_price(
            spot=spot,
            strike=strike,
            rate=rate,
            volatility=volatility,
            time_to_maturity=time_to_maturity,
            dividend_yield=dividend_yield,
        )

    else:

        raise ValueError(
            f"Unsupported option type: "
            f"{option_type}"
        )

    return unit_price * quantity

def calculate_option_risk(
    option_type: str,
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float,
    quantity: float,
):

    greeks = option_greeks(
        option_type=option_type,
        spot=spot,
        strike=strike,
        rate=rate,
        volatility=volatility,
        time_to_maturity=time_to_maturity,
        dividend_yield=dividend_yield,
    )

    return {
        "delta": greeks["delta"] * quantity,
        "gamma": greeks["gamma"] * quantity,
        "vega": greeks["vega"] * quantity,
        "rho": greeks["rho"] * quantity,
        "theta": greeks["theta"] * quantity,
    }

def value_equity(
    spot: float,
    quantity: float,
):

    return spot * quantity

def value_bond(
    face_value: float,
    coupon_rate: float,
    yield_rate: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
):

    periods = int(
        round(
            years_to_maturity
            * coupon_frequency
        )
    )

    if periods <= 0:
        raise ValueError(
            "Bond must have positive maturity."
        )

    periodic_coupon = (
        face_value
        * coupon_rate
        / coupon_frequency
    )

    periodic_yield = (
        yield_rate
        / coupon_frequency
    )

    coupon_pv = sum(
        periodic_coupon
        / (
            1 + periodic_yield
        ) ** period
        for period in range(
            1,
            periods + 1,
        )
    )

    principal_pv = (
        face_value
        / (
            1 + periodic_yield
        ) ** periods
    )

    return coupon_pv + principal_pv
def bond_dv01(
    face_value: float,
    coupon_rate: float,
    yield_rate: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
):

    base_value = value_bond(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_rate=yield_rate,
        years_to_maturity=years_to_maturity,
        coupon_frequency=coupon_frequency,
    )

    bumped_value = value_bond(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_rate=yield_rate + 0.0001,
        years_to_maturity=years_to_maturity,
        coupon_frequency=coupon_frequency,
    )

    dv01 = (
        bumped_value
        - base_value
    )

    return dv01

def value_portfolio(valuation_date=None):

    market_data = load_market_data()

    portfolio = load_portfolio()

    if valuation_date is None:
        valuation_date = get_valuation_date(
            market_data
        )
    else:
        valuation_date = pd.to_datetime(
            valuation_date
        )

        if valuation_date not in market_data.index:
            raise ValueError(
                f"Valuation date {valuation_date} "
                f"not found in market data."
            )
    rate = get_risk_free_rate(
        market_data,
        valuation_date,
    )

    results = []

    for _, trade in portfolio.iterrows():

        trade_id = trade["trade_id"]

        instrument_type = (
            trade["instrument_type"]
        )

        underlying = trade["underlying"]

        quantity = trade["quantity"]

        spot = get_spot(
            market_data,
            underlying,
            valuation_date,
        )

        result = {
            "valuation_date": valuation_date,
            "trade_id": trade_id,
            "instrument_type": instrument_type,
            "underlying": underlying,
            "quantity": quantity,
            "spot": spot,
            "rate": rate,
            "market_value": None,
            "delta": 0.0,
            "gamma": 0.0,
            "vega": 0.0,
            "rho": 0.0,
            "theta": 0.0,
            "ir_dv01": 0.0,
        }

        if instrument_type == "EQUITY":

            result["market_value"] = (
                value_equity(
                    spot,
                    quantity,
                )
            )

            result["delta"] = quantity

        elif instrument_type in (
            "EUROPEAN_CALL",
            "EUROPEAN_PUT",
        ):

            option_type = (
                "CALL"
                if instrument_type
                == "EUROPEAN_CALL"
                else "PUT"
            )

            maturity = year_fraction(
                valuation_date,
                trade["maturity"],
            )

            market_value = value_option(
                option_type=option_type,
                spot=spot,
                strike=trade["strike"],
                rate=rate,
                volatility=trade["volatility"],
                time_to_maturity=maturity,
                dividend_yield=trade[
                    "dividend_yield"
                ],
                quantity=quantity,
            )

            risk = calculate_option_risk(
                option_type=option_type,
                spot=spot,
                strike=trade["strike"],
                rate=rate,
                volatility=trade["volatility"],
                time_to_maturity=maturity,
                dividend_yield=trade[
                    "dividend_yield"
                ],
                quantity=quantity,
            )

            result["market_value"] = (
                market_value
            )

            result["delta"] = (
                risk["delta"]
            )

            result["gamma"] = (
                risk["gamma"]
            )

            result["vega"] = (
                risk["vega"]
            )

            result["rho"] = (
                risk["rho"]
            )

            result["theta"] = (
                risk["theta"]
            )

        elif instrument_type == "BOND":

            maturity = year_fraction(
                valuation_date,
                trade["maturity"],
            )

            market_value = value_bond(
                face_value=quantity,
                coupon_rate=trade[
                    "coupon_rate"
                ],
                yield_rate=rate,
                years_to_maturity=maturity,
                coupon_frequency=trade[
                    "coupon_frequency"
                ],
            )

            result["market_value"] = (
                market_value
            )

            result["ir_dv01"] = (
                bond_dv01(
                    face_value=quantity,
                    coupon_rate=trade[
                        "coupon_rate"
                    ],
                    yield_rate=rate,
                    years_to_maturity=maturity,
                    coupon_frequency=trade[
                        "coupon_frequency"
                    ],
                )
            )

        elif instrument_type == "FX_FORWARD":

            strike = trade["strike"]

            maturity = year_fraction(
                valuation_date,
                trade["maturity"],
            )

            domestic_rate = trade.get(
                "domestic_rate",
                rate,
            )

            foreign_rate = trade.get(
                "foreign_rate",
                0.0,
            )

            market_value = forward_value(
                spot=spot,
                strike=strike,
                domestic_rate=domestic_rate,
                foreign_rate=foreign_rate,
                maturity=maturity,
                notional=quantity,
            )

            result["market_value"] = market_value
            result["delta"] = quantity

        else:

            raise ValueError(
                f"Unsupported instrument: "
                f"{instrument_type}"
            )

        results.append(result)

    return pd.DataFrame(results)


if __name__ == "__main__":

    result = value_portfolio(valuation_date="2025-01-02")

    print(
        result.to_string(
            index=False
        )
    )
import math

from scipy.stats import norm


def _validate_inputs(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
):
    if spot <= 0:
        raise ValueError("Spot price must be positive.")

    if strike <= 0:
        raise ValueError("Strike must be positive.")

    if volatility <= 0:
        raise ValueError("Volatility must be positive.")

    if time_to_maturity <= 0:
        raise ValueError(
            "Time to maturity must be positive."
        )


def d1(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float = 0.0,
) -> float:

    _validate_inputs(
        spot,
        strike,
        rate,
        volatility,
        time_to_maturity,
    )

    numerator = (
        math.log(spot / strike)
        + (
            rate
            - dividend_yield
            + 0.5 * volatility**2
        )
        * time_to_maturity
    )

    denominator = (
        volatility
        * math.sqrt(time_to_maturity)
    )

    return numerator / denominator


def d2(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float = 0.0,
) -> float:

    return (
        d1(
            spot,
            strike,
            rate,
            volatility,
            time_to_maturity,
            dividend_yield,
        )
        - volatility
        * math.sqrt(time_to_maturity)
    )


def call_price(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float = 0.0,
) -> float:

    d1_value = d1(
        spot,
        strike,
        rate,
        volatility,
        time_to_maturity,
        dividend_yield,
    )

    d2_value = d2(
        spot,
        strike,
        rate,
        volatility,
        time_to_maturity,
        dividend_yield,
    )

    return (
        spot
        * math.exp(
            -dividend_yield
            * time_to_maturity
        )
        * norm.cdf(d1_value)
        - strike
        * math.exp(
            -rate
            * time_to_maturity
        )
        * norm.cdf(d2_value)
    )


def put_price(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float = 0.0,
) -> float:

    d1_value = d1(
        spot,
        strike,
        rate,
        volatility,
        time_to_maturity,
        dividend_yield,
    )

    d2_value = d2(
        spot,
        strike,
        rate,
        volatility,
        time_to_maturity,
        dividend_yield,
    )

    return (
        strike
        * math.exp(
            -rate
            * time_to_maturity
        )
        * norm.cdf(-d2_value)
        - spot
        * math.exp(
            -dividend_yield
            * time_to_maturity
        )
        * norm.cdf(-d1_value)
    )
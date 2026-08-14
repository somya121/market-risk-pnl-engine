import math

from scipy.stats import norm


def option_greeks(
    option_type: str,
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_maturity: float,
    dividend_yield: float = 0.0,
) -> dict:

    if time_to_maturity <= 0:
        raise ValueError(
            "Time to maturity must be positive."
        )

    if volatility <= 0:
        raise ValueError(
            "Volatility must be positive."
        )

    sqrt_t = math.sqrt(
        time_to_maturity
    )

    d1 = (
        math.log(spot / strike)
        + (
            rate
            - dividend_yield
            + 0.5 * volatility**2
        )
        * time_to_maturity
    ) / (
        volatility * sqrt_t
    )

    d2 = (
        d1
        - volatility * sqrt_t
    )

    pdf_d1 = norm.pdf(d1)

    discount_rate = math.exp(
        -rate * time_to_maturity
    )

    discount_dividend = math.exp(
        -dividend_yield
        * time_to_maturity
    )

    gamma = (
        discount_dividend
        * pdf_d1
        / (
            spot
            * volatility
            * sqrt_t
        )
    )

    vega = (
        spot
        * discount_dividend
        * pdf_d1
        * sqrt_t
    )

    if option_type == "CALL":

        delta = (
            discount_dividend
            * norm.cdf(d1)
        )

        rho = (
            strike
            * time_to_maturity
            * discount_rate
            * norm.cdf(d2)
        )

        theta = (
            -(
                spot
                * discount_dividend
                * pdf_d1
                * volatility
                / (2 * sqrt_t)
            )
            - (
                rate
                * strike
                * discount_rate
                * norm.cdf(d2)
            )
            + (
                dividend_yield
                * spot
                * discount_dividend
                * norm.cdf(d1)
            )
        )

    elif option_type == "PUT":

        delta = (
            -discount_dividend
            * norm.cdf(-d1)
        )

        rho = (
            -strike
            * time_to_maturity
            * discount_rate
            * norm.cdf(-d2)
        )

        theta = (
            -(
                spot
                * discount_dividend
                * pdf_d1
                * volatility
                / (2 * sqrt_t)
            )
            + (
                rate
                * strike
                * discount_rate
                * norm.cdf(-d2)
            )
            - (
                dividend_yield
                * spot
                * discount_dividend
                * norm.cdf(-d1)
            )
        )

    else:
        raise ValueError(
            "option_type must be CALL or PUT."
        )

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "rho": rho,
        "theta": theta,
        "d1": d1,
        "d2": d2,
    }
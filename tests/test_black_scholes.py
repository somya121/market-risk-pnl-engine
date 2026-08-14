from src.pricing.black_scholes import (
    call_price,
    put_price,
)


def test_call_price_is_positive():

    price = call_price(
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert price > 0


def test_put_price_is_positive():

    price = put_price(
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert price > 0


def test_put_call_parity():

    spot = 200
    strike = 200
    rate = 0.05
    volatility = 0.30
    maturity = 1
    dividend = 0.01

    call = call_price(
        spot,
        strike,
        rate,
        volatility,
        maturity,
        dividend,
    )

    put = put_price(
        spot,
        strike,
        rate,
        volatility,
        maturity,
        dividend,
    )

    lhs = (
        call
        + strike
        * 2.718281828459045
        ** (-rate * maturity)
    )

    rhs = (
        put
        + spot
        * 2.718281828459045
        ** (-dividend * maturity)
    )

    assert abs(lhs - rhs) < 1e-5
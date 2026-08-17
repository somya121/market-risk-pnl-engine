import math

from src.pricing.black_scholes import (
    call_price,
    put_price,
)


def test_call_price_positive():

    price = call_price(
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert price > 0


def test_put_price_positive():

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
        + strike * math.exp(-rate * maturity)
    )

    rhs = (
        put
        + spot * math.exp(-dividend * maturity)
    )

    assert math.isclose(
        lhs,
        rhs,
        rel_tol=1e-10,
    )


def test_call_price_known_value():

    value = call_price(
        spot=100,
        strike=100,
        rate=0.05,
        volatility=0.20,
        time_to_maturity=1,
        dividend_yield=0.0,
    )

    expected = 10.450583572185565

    assert math.isclose(
        value,
        expected,
        rel_tol=1e-8,
    )


def test_put_price_known_value():

    value = put_price(
        spot=100,
        strike=100,
        rate=0.05,
        volatility=0.20,
        time_to_maturity=1,
        dividend_yield=0.0,
    )

    expected = 5.573526022256971

    assert math.isclose(
        value,
        expected,
        rel_tol=1e-8,
    )
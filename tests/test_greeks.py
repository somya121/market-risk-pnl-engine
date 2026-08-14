from src.pricing.greeks import (
    option_greeks,
)


def test_call_delta_is_between_zero_and_one():

    greeks = option_greeks(
        option_type="CALL",
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert 0 < greeks["delta"] < 1


def test_put_delta_is_negative():

    greeks = option_greeks(
        option_type="PUT",
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert greeks["delta"] < 0


def test_gamma_is_positive():

    greeks = option_greeks(
        option_type="CALL",
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert greeks["gamma"] > 0


def test_vega_is_positive():

    greeks = option_greeks(
        option_type="CALL",
        spot=200,
        strike=200,
        rate=0.05,
        volatility=0.30,
        time_to_maturity=1,
        dividend_yield=0.01,
    )

    assert greeks["vega"] > 0
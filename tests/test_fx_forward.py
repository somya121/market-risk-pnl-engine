import math

from src.fx_forward import (
    forward_price,
    forward_value,
)


def test_forward_price():
    spot = 1.10
    domestic_rate = 0.05
    foreign_rate = 0.03
    maturity = 1.0

    expected = (
        spot
        * ((1 + domestic_rate) / (1 + foreign_rate))
        ** maturity
    )

    actual = forward_price(
        spot,
        domestic_rate,
        foreign_rate,
        maturity,
    )

    assert math.isclose(
        actual,
        expected,
        rel_tol=1e-12,
    )


def test_forward_value_is_discounted():
    spot = 1.10
    strike = 1.10
    domestic_rate = 0.05
    foreign_rate = 0.03
    maturity = 1.0
    notional = 2_000_000

    forward = forward_price(
        spot,
        domestic_rate,
        foreign_rate,
        maturity,
    )

    discount_factor = (
        1 / (1 + domestic_rate) ** maturity
    )

    expected = (
        forward - strike
    ) * notional * discount_factor

    actual = forward_value(
        spot,
        strike,
        domestic_rate,
        foreign_rate,
        maturity,
        notional,
    )

    assert math.isclose(
        actual,
        expected,
        rel_tol=1e-12,
    )


def test_at_the_money_forward_value_is_near_zero():
    spot = 1.10
    domestic_rate = 0.05
    foreign_rate = 0.03
    maturity = 1.0

    strike = forward_price(
        spot,
        domestic_rate,
        foreign_rate,
        maturity,
    )

    value = forward_value(
        spot,
        strike,
        domestic_rate,
        foreign_rate,
        maturity,
        2_000_000,
    )

    assert abs(value) < 1e-8
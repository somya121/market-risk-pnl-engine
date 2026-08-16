from src.fx_forward import (
    forward_price,
    forward_value,
)


def test_forward_price_is_positive():

    result = forward_price(
        spot=1.10,
        domestic_rate=0.05,
        foreign_rate=0.02,
        time_to_maturity=1.0,
    )

    assert result > 0


def test_forward_value_is_numeric():

    result = forward_value(
        spot=1.10,
        strike=1.08,
        domestic_rate=0.05,
        foreign_rate=0.02,
        time_to_maturity=1.0,
        notional=1_000_000,
    )

    assert isinstance(
        result,
        float,
    )
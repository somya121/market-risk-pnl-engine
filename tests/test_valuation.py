import math

from src.pricing.valuation import (
    value_bond,
    bond_dv01,
)


def test_bond_value_is_positive():

    value = value_bond(
        face_value=1_000_000,
        coupon_rate=0.04,
        yield_rate=0.04,
        years_to_maturity=10,
        coupon_frequency=2,
    )

    assert value > 0


def test_bond_at_par():

    value = value_bond(
        face_value=1_000_000,
        coupon_rate=0.04,
        yield_rate=0.04,
        years_to_maturity=10,
        coupon_frequency=2,
    )

    assert math.isclose(
        value,
        1_000_000,
        rel_tol=1e-10,
    )


def test_bond_dv01_is_positive():

    dv01 = bond_dv01(
        face_value=1_000_000,
        coupon_rate=0.04,
        yield_rate=0.04,
        years_to_maturity=10,
        coupon_frequency=2,
    )

    assert dv01 > 0
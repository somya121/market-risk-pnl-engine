from src.pricing.valuation import (
    value_portfolio,
)


def test_portfolio_valuation():

    result = value_portfolio()

    assert not result.empty

    assert "market_value" in (
        result.columns
    )

    assert (
        result["market_value"]
        .notna()
        .all()
    )


def test_all_instruments_valued():

    result = value_portfolio()

    expected = {
        "EQUITY",
        "EUROPEAN_CALL",
        "EUROPEAN_PUT",
        "BOND",
        "FX_FORWARD",
    }

    actual = set(
        result["instrument_type"]
    )

    assert expected == actual
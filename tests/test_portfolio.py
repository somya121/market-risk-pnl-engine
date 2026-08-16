import pandas as pd
import pytest

from src.portfolio import validate_portfolio


def test_valid_portfolio():

    portfolio = pd.DataFrame([
        {
            "trade_id": "OPT001",
            "instrument_type": "EUROPEAN_CALL",
            "underlying": "AAPL",
            "quantity": 10,
            "strike": 220,
            "maturity": "2026-12-18",
            "volatility": 0.30,
            "dividend_yield": 0.005,
        }
    ])

    validate_portfolio(portfolio)


def test_option_missing_volatility():

    portfolio = pd.DataFrame([
        {
            "trade_id": "OPT001",
            "instrument_type": "EUROPEAN_CALL",
            "underlying": "AAPL",
            "quantity": 10,
            "strike": 220,
            "maturity": "2026-12-18",
            "volatility": None,
            "dividend_yield": 0.005,
        }
    ])

    with pytest.raises(ValueError):
        validate_portfolio(portfolio)
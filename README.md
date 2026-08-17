# Market Risk & P&L Engine

An end-to-end Python-based market risk engine for portfolio valuation, risk sensitivities, historical P&L, VaR, stress testing, risk limits, and P&L attribution.

## Features

- Multi-asset valuation: **Equities, European Options, Bonds, FX Forwards**
- Black-Scholes pricing and **Greeks**
- Historical **Daily P&L**
- **99% Historical VaR & Expected Shortfall**
- Market **Stress Testing**
- Configurable **Risk Limits & Breach Monitoring**
- Sensitivity-based **P&L Attribution**
- Automated risk metrics and commentary

## Architecture

```text
                 Market Data
                     │
                     ▼
            Portfolio Validation
                     │
                     ▼
             Portfolio Valuation
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Greeks      Daily P&L   Stress
          │          │          │
          └──────────┼──────────┘
                     ▼
              Risk Analytics
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
         VaR      Risk Limits   PLA
          │          │          │
          └──────────┼──────────┘
                     ▼
             Risk Reporting

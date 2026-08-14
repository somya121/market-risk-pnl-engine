def generate_commentary(
    var_99,
    es_99,
    worst_daily_pnl,
    worst_stress_pnl,
    breaches,
    warnings,
):

    commentary = []

    commentary.append(
        f"99% historical VaR is "
        f"{var_99:,.2f}."
    )

    commentary.append(
        f"99% Expected Shortfall is "
        f"{es_99:,.2f}."
    )

    commentary.append(
        f"The worst observed daily P&L "
        f"was {worst_daily_pnl:,.2f}."
    )

    commentary.append(
        f"The worst configured stress "
        f"scenario produced P&L of "
        f"{worst_stress_pnl:,.2f}."
    )

    if breaches > 0:
        commentary.append(
            f"There are {breaches} active "
            f"risk-limit breaches requiring "
            f"attention."
        )
    elif warnings > 0:
        commentary.append(
            f"There are {warnings} risk-limit "
            f"warnings."
        )
    else:
        commentary.append(
            "No configured risk limits are "
            "currently breached."
        )

    return " ".join(commentary)
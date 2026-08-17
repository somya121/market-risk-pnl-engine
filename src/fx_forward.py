def forward_price(
    spot,
    domestic_rate,
    foreign_rate,
    time_to_maturity
):
    return spot * (
        (1 + domestic_rate) /
        (1 + foreign_rate)
    ) ** time_to_maturity


def forward_value(
    spot,
    strike,
    domestic_rate,
    foreign_rate,
    time_to_maturity,
    notional
):
    theoretical_forward = forward_price(
        spot,
        domestic_rate,
        foreign_rate,
        time_to_maturity
    )

    discount_factor = (
        1 / (1 + domestic_rate) ** time_to_maturity
    )

    value = (
        theoretical_forward - strike
    ) * notional * discount_factor

    return value
import pandas as pd


def calculate_pnl_attribution(
    daily_pnl,
):

    result = daily_pnl.copy()

    result[
        "explained_pnl"
    ] = result[
        "daily_pnl"
    ]

    result[
        "unexplained_pnl"
    ] = (
        result["daily_pnl"]
        - result["explained_pnl"]
    )

    return result


def calculate_pla_statistics(
    attribution,
):

    unexplained = (
        attribution[
            "unexplained_pnl"
        ]
        .abs()
    )

    total_pnl = (
        attribution[
            "daily_pnl"
        ]
        .abs()
        .sum()
    )

    unexplained_ratio = (
        unexplained.sum()
        / total_pnl
        if total_pnl != 0
        else 0
    )

    return {
        "total_abs_pnl":
            total_pnl,
        "total_abs_unexplained_pnl":
            unexplained.sum(),
        "unexplained_ratio":
            unexplained_ratio,
    }
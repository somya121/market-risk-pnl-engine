from src.portfolio import (
    load_portfolio,
    validate_portfolio,
)

from src.risk.risk_report import (
    generate_risk_report,
)

from src.risk.portfolio_sensitivities import (
    generate_sensitivity_report,
)

from src.pnl.daily_pnl import (
    save_daily_pnl,
)

from src.risk.risk_metrics_reports import (
    generate_risk_metrics,
)

from src.risk.stress_testing import (
    run_stress_scenarios,
)

from src.risk.risk_limits_report import (
    generate_risk_limit_report,
)

from src.risk.dashboard_metrics import (
    build_dashboard_metrics,
)

from src.risk.risk_commentary import (
    generate_commentary,
)

from src.risk.pla import (
    calculate_pnl_attribution,
    calculate_pla_statistics,
)

import pandas as pd

from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parent

REPORT_DIR = (
    PROJECT_ROOT / "reports"
)


def main():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "\nSTEP 1 - Portfolio validation"
    )

    portfolio = load_portfolio()

    validate_portfolio(
        portfolio
    )

    print(
        "\nSTEP 2 - Portfolio valuation"
    )

    generate_risk_report()

    print(
        "\nSTEP 3 - Portfolio sensitivities"
    )

    generate_sensitivity_report()

    print(
        "\nSTEP 4 - Daily P&L"
    )

    save_daily_pnl()

    print(
        "\nSTEP 5 - Risk analytics"
    )

    generate_risk_metrics()

    print(
        "\nSTEP 6 - Stress testing"
    )

    stress_results = run_stress_scenarios()

    stress_file = (
        REPORT_DIR
        / "stress_results.csv"
    )

    stress_results.to_csv(
        stress_file,
        index=False,
    )

    print(
        "\nSTEP 7 - Risk limits"
    )

    generate_risk_limit_report()

    print(
        "\nSTEP 8 - PLA"
    )

    daily_pnl = pd.read_csv(
        REPORT_DIR
        / "daily_pnl.csv"
    )

    attribution = (
        calculate_pnl_attribution(
            daily_pnl
        )
    )

    attribution.to_csv(
        REPORT_DIR
        / "pnl_attribution.csv",
        index=False,
    )

    pla_stats = (
        calculate_pla_statistics(
            attribution
        )
    )

    print(
        pla_stats
    )

    print(
        "\nSTEP 9 - Dashboard metrics"
    )

    metrics = (
        build_dashboard_metrics()
    )

    print(metrics)

    print(
        "\nSTEP 10 - Risk commentary"
    )

    commentary = generate_commentary(
        var_99=metrics["var_99"],
        es_99=metrics["es_99"],
        worst_daily_pnl=metrics[
            "worst_daily_pnl"
        ],
        worst_stress_pnl=metrics[
            "worst_stress_pnl"
        ],
        breaches=metrics[
            "breaches"
        ],
        warnings=metrics[
            "warnings"
        ],
    )

    commentary_file = (
        REPORT_DIR
        / "risk_commentary.txt"
    )

    with open(
        commentary_file,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            commentary
        )

    print(
        f"\nReports saved to: "
        f"{REPORT_DIR}"
    )


if __name__ == "__main__":
    main()
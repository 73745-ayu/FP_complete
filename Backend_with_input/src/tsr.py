import pandas as pd

def compute_tsr(df, base, years):
    R0, M0, E0 = base["revenue_2024"], base["ebitda_margin_2024"], base["ev_ebitda_2024"]
    EV0, D0, S0 = base["ev_2024"], base["net_debt_2024"], base["shares_2024"]
    Y1, D1, S1 = base["div_yield_2026"], base["net_debt_2026"], base["shares_2026"]

    # Compute intermediate CAGRs
    df["cagr_revenue"] = (df["Revenue"] / R0)**(1/years) - 1
    df["cagr_ebitda_margin"] = (df["EBITDA Margin"] / M0)**(1/years) - 1
    df["cagr_ev_ebitda"] = (df["EV/EBITDA"] / E0)**(1/years) - 1

    EV1 = df["Revenue"] * df["EBITDA Margin"] * df["EV/EBITDA"]
    cap0 = EV0 - D0
    cap1 = EV1 - D1

    df["cagr_mktcap_ev"] = ((cap1/EV1) / (cap0/EV0))**(1/years) - 1
    df["cagr_shares"] = (S1 / S0)**(1/years) - 1
    df["dividend_return"] = (Y1 * (cap1 / S1)) / (cap0 / S0)

    # Calculate TSR explicitly using your formula
    df["TSR"] = (
        (1 + df["cagr_revenue"]) *
        (1 + df["cagr_ebitda_margin"]) *
        (1 + df["cagr_ev_ebitda"]) *
        (1 + df["cagr_mktcap_ev"]) *
        (1 + df["cagr_shares"])
    ) - 1 + df["dividend_return"]

    return df

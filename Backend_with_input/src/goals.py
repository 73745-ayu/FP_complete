from builtins import dict,float, list, print, any
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from src.tsr import compute_tsr

def find_equal_p(
    df: pd.DataFrame,
    base: dict,
    years: float,
    tsr_probs: list[float],
    tol: float = 1e-6
) -> pd.DataFrame:
    rev   = df["Revenue"]
    marg  = df["EBITDA Margin"]
    mult  = df["EV/EBITDA"]
    tsr_s = df["TSR"]
    D1 = base["net_debt_2026"]
    S1 = base["shares_2026"]
    Y1 = base["div_yield_2026"]

    def tsr_at(p_input):
        row = pd.DataFrame({
            "Revenue":          [rev.quantile(1-p_input)],
            "EBITDA Margin":    [marg.quantile(1-p_input)],
            "EV/EBITDA":        [mult.quantile(1-p_input)]
        })
        return compute_tsr(row, base, years)["TSR"].iloc[0]

    out = []
    for p in tsr_probs:
        target = tsr_s.quantile(1-p)

        a, b = tol, 1-tol
        fa, fb = tsr_at(a)-target, tsr_at(b)-target
        if fa*fb > 0:
            p_in = 0.5
        else:
            p_in = brentq(lambda x: tsr_at(x)-target, a, b, xtol=tol)

        thr_rev  = rev.quantile(1-p_in)
        thr_marg = marg.quantile(1-p_in)
        thr_mult = mult.quantile(1-p_in)

        out.append({
            "p_tsr": p,
            "Revenue": thr_rev,
            "p_revenue": p_in,
            "EBITDA Margin": thr_marg,
            "p_margin": p_in,
            "EV/EBITDA": thr_mult,
            "p_multiple": p_in,
            "Market Cap": thr_mult*thr_rev*thr_marg - D1,
            "Share price": (thr_mult*thr_rev*thr_marg - D1)/S1,
            "TSR": target,
            "Probability": p_in
        })

    return pd.DataFrame(out).set_index("p_tsr")

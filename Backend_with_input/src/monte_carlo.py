import numpy as np
import pandas as pd

def simulate(company_data, n_simulations):
    rev = np.random.triangular(company_data["Revenue"]["0th"], company_data["Revenue"]["median"], company_data["Revenue"]["100th"], n_simulations)
    marg = np.random.triangular(company_data["EBITDA_Margin"]["0th"], company_data["EBITDA_Margin"]["median"], company_data["EBITDA_Margin"]["100th"], n_simulations)
    mult = np.random.triangular(company_data["EV_EBITDA"]["0th"], company_data["EV_EBITDA"]["median"], company_data["EV_EBITDA"]["100th"], n_simulations)
    
    return pd.DataFrame({
        "Revenue": rev,
        "EBITDA Margin": marg,
        "EV/EBITDA": mult
    })

import numpy as np
import pandas as pd

def consolidate_refinitiv_data(df, key_columns):
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    aggregations = {col: 'first' for col in df.columns if col not in numeric_cols + key_columns}

    for col in numeric_cols:
        aggregations[col] = lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan
    
    return df.groupby(key_columns, as_index=False).agg(aggregations)

def calculate_derived_metrics(df, poa_input):
    revenue_col = f"Revenue {poa_input}"
    ebitda_col = f"EBITDA {poa_input}"
    ebit_col = f"EBIT {poa_input}"
    net_debt_col = f"Net Debt {poa_input}"
    shares_col = f"Shares Outstanding {poa_input}"
    price_col = "Price"
    market_cap_col = f"Market Cap {poa_input}"
    ev_col = f"EV {poa_input}"
    ev_ebitda_col = f"EV/EBITDA {poa_input}"
    dps_col = f"DPS {poa_input}"
    div_yield_col = f"{poa_input} Dividend Yield"

    df[f"EBITDA Margin {poa_input}"] = df[ebitda_col] / df[revenue_col]
    df[f"EBIT Margin {poa_input}"] = df[ebit_col] / df[revenue_col]
    df[market_cap_col] = df[shares_col] * df[price_col]
    df[ev_col] = df[market_cap_col] + df[net_debt_col]
    df[ev_ebitda_col] = df[ev_col] / df[ebitda_col]
    df[div_yield_col] = df[dps_col] / df[price_col]

    return df

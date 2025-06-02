import refinitiv.data as rd
import pandas as pd
from config.column_names import *
from config.overrides import refinitiv_override

def open_refinitiv_session():
    rd.open_session()

def apply_broker_overrides(df):
    df[col_broker_name] = df[col_broker_name].str.upper().str.strip()
    df[col_broker_name] = df[col_broker_name].replace(refinitiv_override)
    return df

def get_metric(metric_code, label, companies, period, scale_on=True):
    scale_str = f",Scale=6" if scale_on else ""
    fields_list = [
        f"{metric_code}.brokername",
        f"{metric_code}.date",
        f"{metric_code}{scale_str}"
    ]

    df = rd.get_data(
        universe=companies,
        fields=fields_list,
        parameters={"Period": period}
    )

    df.columns = [col_ticker, col_broker_name, col_estimate_date, label]
    df = apply_broker_overrides(df)
    df[col_estimate_date] = pd.to_datetime(df[col_estimate_date], errors="coerce").dt.date
    return df.dropna(subset=[col_broker_name, col_estimate_date, label])

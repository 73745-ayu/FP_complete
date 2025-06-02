import pandas as pd

def format_dates(df):
    date_cols = [col for col in df.columns if "Date" in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d %b %y")
    return df

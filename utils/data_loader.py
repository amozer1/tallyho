import pandas as pd

def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

    if "Date of reply (CDE)" in df.columns:
        df["Reply Date"] = pd.to_datetime(df["Date of reply (CDE)"], errors="coerce", dayfirst=True)
    else:
        df["Reply Date"] = None

    return df
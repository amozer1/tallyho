import pandas as pd
from datetime import datetime

def load_data(path="data/TQ_TH.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    for c in ["Date Sent","Required Date","Reply Date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True)

    now = pd.Timestamp(datetime.now())

    df["AgeDays"] = (now - df["Date Sent"]).dt.days
    df["ResponseDays"] = (df["Reply Date"] - df["Date Sent"]).dt.days
    df["ResponseDays"] = df["ResponseDays"].fillna(df["AgeDays"])

    df["Closed"] = df["Reply Date"].notna() | (df["Status"].str.lower()=="closed")
    df["Open"] = ~df["Closed"]
    df["Overdue"] = (df["AgeDays"] > 7) & df["Open"]

    return df
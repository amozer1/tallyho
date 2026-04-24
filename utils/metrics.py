import pandas as pd
from datetime import datetime

def compute_metrics(df):

    now = pd.Timestamp(datetime.now())

    df["AgeDays"] = (now - df["Date Sent"]).dt.days

    tq = df[df["Doc Type"] == "TQ"]
    rfi = df[df["Doc Type"] == "RFI"]

    open_items = df[df["Reply Date"].isna()]
    overdue_7 = df[df["AgeDays"] > 7]
    overdue_30 = df[df["AgeDays"] > 30]

    sla = round((len(df[df["AgeDays"] <= 7]) / len(df)) * 100, 1)

    return {
        "df": df,
        "tq": len(tq),
        "rfi": len(rfi),
        "open": len(open_items),
        "overdue7": len(overdue_7),
        "overdue30": len(overdue_30),
        "sla": sla
    }
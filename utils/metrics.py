import pandas as pd
from datetime import datetime


def compute_metrics(df):
    df = df.copy()

    # -----------------------------
    # SAFETY CHECKS (prevents Streamlit Cloud crashes)
    # -----------------------------
    required_cols = ["Date Sent", "Doc Type", "Sender", "Recipient"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # -----------------------------
    # DATE PROCESSING
    # -----------------------------
    df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

    now = pd.Timestamp(datetime.now())
    df["AgeDays"] = (now - df["Date Sent"]).dt.days

    # -----------------------------
    # OPTIONAL COLUMN HANDLING
    # -----------------------------
    if "Date of reply (CDE)" in df.columns:
        df["Reply Date"] = pd.to_datetime(df["Date of reply (CDE)"], errors="coerce", dayfirst=True)
    else:
        df["Reply Date"] = pd.NaT

    # -----------------------------
    # CORE FILTERS
    # -----------------------------
    tq = df[df["Doc Type"] == "TQ"]
    rfi = df[df["Doc Type"] == "RFI"]

    open_items = df[df["Reply Date"].isna()]
    overdue_7 = df[df["AgeDays"] > 7]
    overdue_30 = df[df["AgeDays"] > 30]

    total = len(df)

    sla_pct = round((len(df[df["AgeDays"] <= 7]) / total) * 100, 1) if total > 0 else 0

    # -----------------------------
    # RETURN CLEAN STRUCTURE
    # -----------------------------
    return {
        "df": df,
        "tq": len(tq),
        "rfi": len(rfi),
        "open": len(open_items),
        "overdue7": len(overdue_7),
        "overdue30": len(overdue_30),
        "sla": sla_pct
    }
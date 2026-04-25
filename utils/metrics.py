import pandas as pd

def get_metrics(df):

    if df is None or df.empty:
        return {
            "total_tq": 0,
            "total_rfi": 0,
            "closed": 0,
            "open": 0,
            "overdue7": 0,
            "avg_response": 0,
            "sla": 0
        }

    df = df.copy()

    # =========================
    # SAFE COLUMN HANDLING
    # =========================
    if "AgeDays" not in df.columns:
        df["AgeDays"] = 0
    else:
        df["AgeDays"] = pd.to_numeric(df["AgeDays"], errors="coerce").fillna(0)

    if "ResponseDays" not in df.columns:
        df["ResponseDays"] = 0
    else:
        df["ResponseDays"] = pd.to_numeric(df["ResponseDays"], errors="coerce").fillna(0)

    # =========================
    # SAFE TEXT FIELDS
    # =========================
    df["Type"] = df.get("Doc Type", df.get("Type", "")).astype(str)
    df["Status"] = df.get("Status", "").astype(str)

    # =========================
    # CORE METRICS (YOUR DATA ONLY)
    # =========================
    total_tq = len(df[df["Type"].str.upper() == "TQ"])
    total_rfi = len(df[df["Type"].str.upper() == "RFI"])

    closed = len(df[df["Status"].str.lower() == "closed"])
    open_items = len(df[df["Status"].str.lower() != "closed"])

    overdue7 = len(df[df["AgeDays"] > 7])

    avg_response = round(df["ResponseDays"].mean(), 1) if len(df) > 0 else 0

    sla = round((len(df[df["ResponseDays"] <= 7]) / len(df)) * 100, 1) if len(df) > 0 else 0

    return {
        "total_tq": total_tq,
        "total_rfi": total_rfi,
        "closed": closed,
        "open": open_items,
        "overdue7": overdue7,
        "avg_response": avg_response,
        "sla": sla
    }
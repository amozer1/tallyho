import pandas as pd

def load_data():

    file_path = "data/TQ_TH.xlsx"

    df = pd.read_excel(file_path)

    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    df.columns = df.columns.str.strip()

    # =========================
    # FIX DATES (YOUR REAL COLUMNS)
    # =========================
    date_cols = ["Date Sent", "Required Date", "Reply Date"]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # =========================
    # DERIVED METRICS (SAFE)
    # =========================
    today = pd.Timestamp.today().normalize()

    df["AgeDays"] = (today - df["Date Sent"]).dt.days

    df["IsClosed"] = df["Reply Date"].notna()

    df["IsOverdue"] = (df["AgeDays"] > 7) & (~df["IsClosed"])

    # SLA logic (based on Required Date)
    df["MissedSLA"] = (
        df["Reply Date"].isna() &
        (df["Required Date"] < today)
    )

    return df
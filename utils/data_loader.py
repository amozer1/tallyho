import pandas as pd

def load_data():

    file_path = "data/TQ_TH.xlsx"  # GitHub path only

    df = pd.read_excel(file_path)

    df.columns = [c.strip() for c in df.columns]

    # Dates
    for col in ["Date Sent", "Date reply required by", "Date of reply (CDE)"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Derived fields
    today = pd.Timestamp.today()

    df["AgeDays"] = (today - df["Date Sent"]).dt.days
    df["IsClosed"] = df["Date of reply (CDE)"].notna()
    df["IsOverdue"] = (df["AgeDays"] > 7) & (~df["IsClosed"])

    return df
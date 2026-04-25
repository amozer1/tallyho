import pandas as pd
import os
import glob

DATA_FOLDER = "data/"

def load_data():
    files = glob.glob(os.path.join(DATA_FOLDER, "*.xlsx"))

    if not files:
        return pd.DataFrame()

    # always pick latest file
    file_path = max(files, key=os.path.getctime)

    df = pd.read_excel(file_path)

    if df.empty:
        return df

    # clean column names
    df.columns = df.columns.str.strip()

    rename_map = {
        "Doc Type": "Type",
        "Date Sent": "DateSent",
        "Required Date": "RequiredDate",
        "Reply Date": "ReplyDate"
    }

    df.rename(columns=rename_map, inplace=True)

    # ensure required columns exist
    for col in ["Type", "DateSent", "ReplyDate", "RequiredDate"]:
        if col not in df.columns:
            df[col] = pd.NA

    # date parsing
    for c in ["DateSent", "RequiredDate", "ReplyDate"]:
        df[c] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")

    today = pd.Timestamp.today().normalize()

    # ---------------- FEATURES (ML READY) ----------------

    df["AgeDays"] = (today - df["DateSent"]).dt.days
    df["AgeDays"] = df["AgeDays"].fillna(0)

    df["ResponseDays"] = (df["ReplyDate"] - df["DateSent"]).dt.days
    df["ResponseDays"] = df["ResponseDays"].fillna(0)

    df["Outstanding"] = df["ReplyDate"].isna()

    df["Overdue"] = (
        (df["RequiredDate"].notna()) &
        (today > df["RequiredDate"]) &
        (df["Outstanding"])
    )

    # ML safety cleanup
    df["AgeDays"] = pd.to_numeric(df["AgeDays"], errors="coerce").fillna(0)
    df["ResponseDays"] = pd.to_numeric(df["ResponseDays"], errors="coerce").fillna(0)

    return df
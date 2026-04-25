import pandas as pd
import os
from datetime import datetime

def load_data():
    file_path = "data/TQ_TH.xlsx"

    if not os.path.exists(file_path):
        return pd.DataFrame()

    df = pd.read_excel(file_path)

    # Standardise column names
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        "Doc Type": "Type",
        "Date Sent": "DateSent",
        "Required Date": "RequiredDate",
        "Reply Date": "ReplyDate"
    }

    df.rename(columns=rename_map, inplace=True)

    # Parse dates
    for c in ["DateSent", "RequiredDate", "ReplyDate"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")

    today = pd.Timestamp.today().normalize()

    # Age Days
    if "DateSent" in df.columns:
        df["AgeDays"] = (today - df["DateSent"]).dt.days
    else:
        df["AgeDays"] = 0

    # Response Days
    if "ReplyDate" in df.columns:
        df["ResponseDays"] = (df["ReplyDate"] - df["DateSent"]).dt.days
    else:
        df["ResponseDays"] = 0

    # Outstanding
    df["Outstanding"] = df["ReplyDate"].isna()

    # Overdue
    if "RequiredDate" in df.columns:
        df["Overdue"] = (today > df["RequiredDate"]) & (df["Outstanding"])
    else:
        df["Overdue"] = False

    return df
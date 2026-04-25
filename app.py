import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.tracker import render_tracker
from components.overdue_alert import render_overdue_alert


st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

# =========================
# UI
# =========================
render_sidebar()
render_header()

# =========================
# DATA LOAD
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")

df = load_data()

# =========================
# CLEAN DATA
# =========================
df = df.copy()
df.columns = [c.strip().lower() for c in df.columns]

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

today = pd.Timestamp.today().normalize()
df["age"] = (today - df["date sent"]).dt.days

total = len(df)

tq = df[df["doc type"].str.lower() == "tq"]
rfi = df[df["doc type"].str.lower() == "rfi"]

tq_not = len(tq[tq["reply date"].isna()])
rfi_not = len(rfi[rfi["reply date"].isna()])

tq_total = len(tq)
rfi_total = len(rfi)

tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0

overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

# =========================
# ALERT (TOP)
# =========================
render_overdue_alert(
    overdue=overdue,
    total=total,
    tq_not=tq_not,
    rfi_not=rfi_not,
    tq_not_pct=tq_not_pct,
    rfi_not_pct=rfi_not_pct
)

# =========================
# MAIN DASHBOARD
# =========================
render_tracker(df)
import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.tracker import render_tracker
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding
from components.trend import render_trend


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

# =========================
# UI FRAMEWORK
# =========================
render_sidebar()
render_header()

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")


df = load_data()

# =========================
# CLEAN DATA (GLOBAL)
# =========================
df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

today = pd.Timestamp.today().normalize()
df["age"] = (today - df["date sent"]).dt.days


# =========================
# DASHBOARD TITLE BLOCK
# (optional lightweight header inside body)
# =========================
st.markdown("## 📊 TQ / RFI Control Dashboard")


# =========================
# 2×2 CONTROL GRID (MAIN CHANGE)
# =========================
row1_col1, row1_col2 = st.columns(2, gap="large")

with row1_col1:
    render_trend(df)

with row1_col2:
    render_outstanding_line(df, total=len(df))


row2_col1, row2_col2 = st.columns(2, gap="large")

with row2_col1:
    render_age_outstanding(df)

with row2_col2:
    render_tracker(df)
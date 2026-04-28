import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.trend import render_trend
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="TQ / RFI Dashboard", layout="wide")

render_sidebar()
render_header()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")

df = load_data()

df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

# =========================
# LAYOUT
# LEFT = Outstanding (full focus)
# RIGHT = Age (top) + Trend (bottom)
# =========================
col_left, col_right = st.columns([1.4, 1], gap="large")

# =========================
# LEFT COLUMN
# =========================
with col_left:
    render_outstanding_line(df, total=len(df))

# =========================
# RIGHT COLUMN (STACKED)
# =========================
with col_right:
    render_age_outstanding(df)
    st.markdown("---")  # visual separator
    render_trend(df)
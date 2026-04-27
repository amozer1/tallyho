import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.trend import render_trend
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding
from components.tracker import render_tracker


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

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
# BOARD TITLE
# =========================
st.markdown("## 📊 TQ / RFI Control Board")


# =========================
# ROW 1 (BIG IMPACT VISUALS)
# =========================
col1, col2 = st.columns([1.4, 1], gap="large")

with col1:
    render_trend(df)   # BIGGEST visual (trend always dominates)

with col2:
    render_outstanding_line(df, total=len(df))


# =========================
# ROW 2 (SUPPORTING INTELLIGENCE)
# =========================
col3, col4 = st.columns([1, 1.2], gap="large")

with col3:
    render_age_outstanding(df)

with col4:
    render_tracker(df)
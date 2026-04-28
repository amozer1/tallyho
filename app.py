import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.trend import render_trend
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding

st.set_page_config(page_title="TQ / RFI Dashboard", layout="wide")

render_sidebar()
render_header()

@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")

df = load_data()

df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

# =========================
# 4 EQUAL DASHBOARD LAYOUT
# =========================
col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    render_outstanding_line(df, total=len(df))

with col2:
    render_trend(df)

with col3:
    render_age_outstanding(df)

with col4:
    st.info("KPI / Summary Panel (Future Use)")
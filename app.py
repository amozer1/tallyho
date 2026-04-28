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
# ROW 1 (OUTSTANDING - 2 CARDS SIDE BY SIDE)
# =========================
top_col1, top_col2 = st.columns(2, gap="large")

with top_col1:
    render_outstanding_line(df, total=len(df))

with top_col2:
    render_outstanding_line(df, total=len(df))  # or second variant if you have TQ vs RFI split later

# =========================
# ROW 2 (ANALYTICS)
# =========================
bottom_col1, bottom_col2 = st.columns(2, gap="large")

with bottom_col1:
    render_trend(df)

with bottom_col2:
    render_age_outstanding(df)
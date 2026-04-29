import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.trend import render_trend
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding

# =========================
# PAGE CONFIG + WHITE THEME
# =========================
st.set_page_config(page_title="TQ / RFI Dashboard", layout="wide")

# Force white background for entire app
st.markdown(
    """
    <style>
        .stApp {
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER / SIDEBAR
# =========================
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
# TOP: OUTSTANDING (FULL WIDTH)
# =========================
render_outstanding_line(df, total=len(df))

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# BOTTOM: AGE + TREND
# =========================
col_left, col_right = st.columns(2, gap="large")

with col_left:
    render_age_outstanding(df)

with col_right:
    render_trend(df)
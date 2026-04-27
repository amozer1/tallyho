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
# CSS FOR EQUAL PANELS
# =========================
st.markdown("""
<style>
.equal-panel {
    background: white;
    border-radius: 14px;
    padding: 14px;
    height: 460px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    overflow: hidden;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

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
# CLEAN DATA
# =========================
df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

today = pd.Timestamp.today().normalize()
df["age"] = (today - df["date sent"]).dt.days

# =========================
# TITLE
# =========================
st.markdown("## 📊 TQ / RFI Control Dashboard")

# =========================
# GRID
# =========================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="equal-panel">', unsafe_allow_html=True)
    render_trend(df)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="equal-panel">', unsafe_allow_html=True)
    render_outstanding_line(df, total=len(df))
    st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown('<div class="equal-panel">', unsafe_allow_html=True)
    render_age_outstanding(df)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="equal-panel">', unsafe_allow_html=True)
    render_tracker(df)
    st.markdown('</div>', unsafe_allow_html=True)
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
st.set_page_config(
    page_title="Tally Ho TQ & RFI Tracker",
    layout="wide"
)


# =========================
# LOAD DATA (MULTI-ASSET)
# =========================
@st.cache_data
def load_data():
    return {
        "Newlay CSO": pd.read_excel("data/newlay.xlsx"),
        "Eureca": pd.read_excel("data/eureca.xlsx"),
        "Musa": pd.read_excel("data/musa.xlsx"),
        "Juli": pd.read_excel("data/juli.xlsx"),
    }


datasets = load_data()


# =========================
# SIDEBAR (NOW WORKS)
# =========================
asset, df, seq = render_sidebar(datasets)

render_header()


# =========================
# CLEAN SELECTED DATA ONLY
# =========================
df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")


# =========================
# DEFAULT DASHBOARD VIEW
# =========================
st.title(f"{asset} Tracker")

render_outstanding_line(df, total=len(df))

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    render_trend(df)

with col2:
    render_age_outstanding(df)


# =========================
# SELECTED ROW VIEW
# =========================
if seq is not None:

    selected = df[df["seq no"] == seq].iloc[0]

    st.markdown("---")
    st.subheader(f"{selected['doc type']} - {selected['seq no']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Originator:**", selected["originator"])
        st.write("**Sender:**", selected["sender"])
        st.write("**Recipient:**", selected["recipient"])

    with col2:
        st.write("**Date Sent:**", selected["date sent"])
        st.write("**Required Date:**", selected["required date"])
        st.write("**Reply Date:**", selected["reply date"])

    st.write("**Subject:**", selected["subject"])
    st.write("**Notes:**", selected["notes"])
    st.write("**Status:**", selected["status"])
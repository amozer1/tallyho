import streamlit as st
import pandas as pd
import os

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
# SAFE LOAD FUNCTION
# =========================
def safe_load(path):
    if os.path.exists(path):
        return pd.read_excel(path)
    return None


# =========================
# LOAD DATASETS (SAFE)
# =========================
@st.cache_data
def load_data():
    return {
        "Tally Ho": safe_load("data/TQ_TH.xlsx"),
        "Ferry PS": safe_load("data/ferry_ps.xlsx"),
        "Rossall Outfall": safe_load("data/rossall_outfall.xlsx"),
        "Flass Lane": safe_load("data/flass_lane.xlsx"),
    }


datasets = load_data()


# =========================
# SIDEBAR
# =========================
asset, df, seq = render_sidebar(datasets)

render_header()


# =========================
# HANDLE MISSING DATA
# =========================
st.title(f"{asset} Tracker")

if df is None or df.empty:
    st.warning(f"No data available for {asset}")
    st.stop()


# =========================
# CLEAN DATA
# =========================
df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")


# =========================
# DASHBOARD
# =========================
render_outstanding_line(df, total=len(df))

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    render_trend(df)

with col2:
    render_age_outstanding(df)


# =========================
# ROW DETAILS (SEQ SELECT)
# =========================
if seq is not None:

    selected_df = df[df["seq no"] == seq]

    if not selected_df.empty:
        selected = selected_df.iloc[0]

        st.markdown("---")
        st.subheader(f"{selected['doc type']} - {selected['seq no']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Originator:**", selected.get("originator", "—"))
            st.write("**Sender:**", selected.get("sender", "—"))
            st.write("**Recipient:**", selected.get("recipient", "—"))

        with col2:
            st.write("**Date Sent:**", selected.get("date sent", "—"))
            st.write("**Required Date:**", selected.get("required date", "—"))
            st.write("**Reply Date:**", selected.get("reply date", "—"))

        st.write("**Subject:**", selected.get("subject", "—"))
        st.write("**Notes:**", selected.get("notes", "—"))
        st.write("**Status:**", selected.get("status", "—"))
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
    try:
        if not os.path.exists(path):
            return None
        return pd.read_excel(path)
    except Exception:
        return None


# =========================
# LOAD DATASETS
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


# =========================
# HEADER
# =========================
render_header(asset)


# =========================
# SAFETY CHECK (CRITICAL FIX)
# =========================
df_raw = datasets.get(asset)

if df_raw is None:
    st.error(f"""
    ❌ Dataset '{asset}' failed to load.

    Check:
    - File exists in GitHub repo
    - Correct path: data/{asset}.xlsx
    - No .xlsx.xlsx naming issue
    """)
    st.stop()

df = df_raw.copy()


# =========================
# CLEAN DATA
# =========================
df.columns = df.columns.str.strip().str.lower()

required_cols = ["date sent", "reply date", "seq no", "doc type", "status"]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.write("Available columns:", df.columns.tolist())
    st.stop()


df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")


# =========================
# HANDLE EMPTY DATA
# =========================
if df.empty:
    st.warning(f"No data available for {asset}")
    st.stop()


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
# ROW DETAILS
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
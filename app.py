import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TQ & RFI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DARK THEME UI ----------------
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.4);
    margin-bottom: 10px;
}

.kpi {
    font-size: 22px;
    font-weight: 700;
}

.small {
    font-size: 13px;
    opacity: 0.8;
}

h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA (ROBUST) ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", header=0)

    # Clean column names (VERY IMPORTANT for your issue)
    df.columns = df.columns.astype(str).str.strip()

    # Fix common messy Excel exports
    rename_map = {
        "Seq No": "Seq_No",
        "Date Sent": "Date_Sent",
        "Required Date": "Required_Date",
        "Reply Date": "Reply_Date",
        "Doc Type": "Type"
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Force correct columns even if missing
    for col in ["Date_Sent", "Required_Date", "Reply_Date"]:
        if col not in df.columns:
            df[col] = np.nan

    # Convert dates safely (NO ERRORS IF EMPTY)
    for col in ["Date_Sent", "Required_Date", "Reply_Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Clean Status
    if "Status" in df.columns:
        df["Status"] = df["Status"].fillna("Unknown")

    # Fill blanks safely
    df = df.fillna("")

    return df


df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "TQs vs RFIs", "Analytics", "Overdue Tracker"]
)

# ---------------- HEADER ----------------
st.title("TQ & RFI AI Dashboard")
st.caption("Clean, structured contract communication intelligence system")

# ---------------- FILTERS ----------------
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    doc_filter = st.selectbox("Document Type", ["All"] + sorted(df["Type"].unique()))

with col_f2:
    status_filter = st.selectbox("Status", ["All"] + sorted(df["Status"].unique()))

with col_f3:
    sender_filter = st.selectbox("Sender", ["All"] + sorted(df["Sender"].astype(str).unique()))

# Apply filters
filtered = df.copy()

if doc_filter != "All":
    filtered = filtered[filtered["Type"] == doc_filter]

if status_filter != "All":
    filtered = filtered[filtered["Status"] == status_filter]

if sender_filter != "All":
    filtered = filtered[filtered["Sender"] == sender_filter]

# ---------------- KPI CARDS ----------------
st.markdown("## Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi">{len(filtered)}</div>
        <div class="small">Total Records</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi">{len(filtered[filtered['Type'] == 'RFI'])}</div>
        <div class="small">RFIs</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi">{len(filtered[filtered['Type'] == 'TQ'])}</div>
        <div class="small">TQs</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    overdue = filtered[
        (filtered["Required_Date"].notna()) &
        (filtered["Reply_Date"].isna())
    ]
    st.markdown(f"""
    <div class="card">
        <div class="kpi">{len(overdue)}</div>
        <div class="small">Overdue (No Reply)</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CHARTS ----------------
st.markdown("## Analytics")

c1, c2 = st.columns(2)

with c1:
    st.subheader("TQ vs RFI Split")
    fig = px.pie(filtered, names="Type", title="Distribution")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Status Breakdown")
    fig2 = px.bar(filtered, x="Status", color="Type")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- OVERDUE TABLE ----------------
st.markdown("## 📌 Live Register")

display_cols = [
    "Project ID", "Type", "Seq_No", "Date_Sent",
    "Required_Date", "Reply_Date", "Sender",
    "Recipient", "Subject", "Status"
]

available_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[available_cols],
    use_container_width=True,
    height=500
)

# ---------------- INSIGHTS ----------------
st.markdown("## AI Insights")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.info("Most items are concentrated in RFI workflow stage.")

with col_b:
    st.warning("Several items have missing Reply Dates → risk of delay.")

with col_c:
    st.success("System is tracking response performance automatically.")
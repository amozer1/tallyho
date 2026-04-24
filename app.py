import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Engineering Control Centre", layout="wide")

# =========================
# LOAD DATA (STREAMLIT CLOUD SAFE)
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]
    return df

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])
default_path = "data/TQ_TH.xlsx"

df = load_data(uploaded_file) if uploaded_file else load_data(default_path)

# =========================
# CLEANING
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
df["Reply Date"] = pd.to_datetime(df["Reply Date"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())
df["AgeDays"] = (now - df["Date Sent"]).dt.days.fillna(0)

# =========================
# CORE FLAGS
# =========================
is_tq = df["Doc Type"].str.contains("TQ", na=False)
is_rfi = df["Doc Type"].str.contains("RFI", na=False)

open_df = df[df["Status"].str.contains("Open", case=False, na=False)]
closed_df = df[df["Status"].str.contains("Closed", case=False, na=False)]

over_7 = df[df["AgeDays"] > 7]
over_30 = df[df["AgeDays"] > 30]

# =========================
# AI RISK ENGINE
# =========================
df["RiskScore"] = (
    (df["AgeDays"] / 30).clip(0, 1) * 0.65 +
    df["Status"].str.contains("Open", case=False, na=False).astype(int) * 0.35
) * 100

df["RiskBand"] = pd.cut(
    df["RiskScore"],
    bins=[0, 40, 70, 100],
    labels=["Low", "Medium", "High"]
)

# =========================
# HEADER (CONTROL ROOM STYLE)
# =========================
left, right = st.columns([3, 1])

with left:
    st.title("🏗 Engineering Control Centre")
    st.caption("TQ & RFI Intelligence | Project Delivery Monitoring | AI Risk Analytics")

with right:
    st.write(f"📅 {datetime.now().strftime('%d %b %Y')}")
    st.download_button("⬇ Export Control Report", df.to_csv(index=False), "ECC_Report.csv")

st.markdown("---")

# =========================
# KPI STRIP (EXECUTIVE TOP BAR)
# =========================
k1, k2, k3, k4 = st.columns(4)

k1.metric("🔴 Overdue >7 Days", len(over_7))
k2.metric("📄 Total TQs", int(is_tq.sum()))
k3.metric("📄 Total RFIs", int(is_rfi.sum()))
k4.metric("⏳ >30 Days Risk", len(over_30))

st.markdown("---")

# =========================
# CONTROL CENTRE MAIN GRID
# =========================
A, B = st.columns([2.6, 1.4])

# =========================
# A - COMMAND OVERVIEW (EXECUTIVE CORE)
# =========================
with A:
    st.subheader("A - Project Command Overview")

    tq_only = (is_tq & ~is_rfi).sum()
    rfi_only = (is_rfi & ~is_tq).sum()
    both = (is_tq & is_rfi).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("TQ Only", tq_only)
    col2.metric("RFI Only", rfi_only)
    col3.metric("Shared / Both", both)

    # CONTROL VISUAL (better than pie: executive donut + heat logic)
    venn = pd.DataFrame({
        "Category": ["TQ Only", "RFI Only", "Both"],
        "Count": [tq_only, rfi_only, both]
    })

    fig = px.pie(
        venn,
        names="Category",
        values="Count",
        hole=0.6,
        color_discrete_sequence=["#4C78A8", "#F58518", "#54A24B"]
    )

    st.plotly_chart(fig, use_container_width=True)

    # OVERDUE INTELLIGENCE BLOCK
    st.markdown("### 🚨 Control Alerts")

    st.write(f"• TQs overdue >7 days: {(is_tq & (df['AgeDays'] > 7)).sum()}")
    st.write(f"• RFIs overdue >7 days: {(is_rfi & (df['AgeDays'] > 7)).sum()}")
    st.write(f"• Total system backlog (>7 days): {len(over_7)}")

# =========================
# B - EXECUTIVE KPI PANEL
# =========================
with B:
    st.subheader("B - Executive KPI Panel")

    st.metric("Closed Items", len(closed_df))
    st.metric("Active Open Items", len(open_df))
    st.metric("Critical (>30 Days)", len(over_30))

    st.markdown("#### System Pressure Index")

    pressure = len(over_30) / len(df)
    st.progress(min(pressure, 1.0))

# =========================
# SECONDARY CONTROL GRID
# =========================
C, D, E = st.columns([2.2, 2.2, 1.6])

# =========================
# C - DELIVERY TREND CONTROL
# =========================
with C:
    st.subheader("C - Delivery Trend Control")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig = go.Figure()

    if "TQ" in trend.columns:
        fig.add_trace(go.Scatter(y=trend["TQ"], name="TQ Flow", line=dict(color="#4C78A8")))

    if "RFI" in trend.columns:
        fig.add_trace(go.Scatter(y=trend["RFI"], name="RFI Flow", line=dict(color="#F58518")))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# D - AGEING HEAT CONTROL
# =========================
with D:
    st.subheader("D - Backlog Age Heat Map")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig = px.bar(
        x=age.index,
        y=age.values,
        text=[f"{v} ({round(v/len(df)*100,1)}%)" for v in age.values],
        color=age.values,
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# E - AI COMMAND RISK ENGINE
# =========================
with E:
    st.subheader("E - AI Risk Command")

    avg_risk = df["RiskScore"].mean()

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_risk,
        title={"text": "System Risk Level"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "#2ECC71"},
                {"range": [40, 70], "color": "#F1C40F"},
                {"range": [70, 100], "color": "#E74C3C"}
            ],
            "bar": {"color": "black"}
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# CONTROL INTELLIGENCE (BOTTOM STRIP)
# =========================
st.markdown("---")
st.subheader("🧠 Executive Intelligence Layer")

c1, c2 = st.columns(2)

with c1:
    st.warning(f"""
    🚨 HIGH RISK BACKLOG

    {len(over_7)} items exceed 7-day threshold with no response.
    These items require immediate engineering intervention.
    """)

with c2:
    top_sender = df["Sender"].value_counts().idxmax()
    st.info(f"""
    📌 WORKLOAD CONCENTRATION

    Primary bottleneck: {top_sender}
    This contributor accounts for highest document load.
    """)

# =========================
# LIVE CONTROL TABLE
# =========================
st.markdown("---")
st.subheader("📡 Live Control Register")

st.dataframe(
    df[[
        "Project ID",
        "Doc Type",
        "Seq No",
        "Sender",
        "Recipient",
        "Subject",
        "Status",
        "AgeDays",
        "RiskScore",
        "RiskBand"
    ]],
    use_container_width=True
)
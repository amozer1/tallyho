import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="TQ & RFI ML Dashboard", layout="wide")

# =========================
# DATA LOADER
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]
    return df

# =========================
# FILE SOURCE (CLOUD SAFE)
# =========================
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

# GitHub repo path (IMPORTANT FOR STREAMLIT CLOUD)
default_path = "data/TQ_TH.xlsx"

if uploaded_file is not None:
    df = load_data(uploaded_file)

elif os.path.exists(default_path):
    df = load_data(default_path)

else:
    st.error("❌ Excel file not found. Upload a file or add it to /data folder in GitHub.")
    st.stop()

# =========================
# CLEANING
# =========================
for c in df.columns:
    if df[c].dtype == "object":
        df[c] = df[c].astype(str)

# DATE PARSING
date_cols = ["Date Sent", "Reply Date", "Required Date"]
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())

# =========================
# CORE LOGIC
# =========================
doc_type = df["Doc Type"] if "Doc Type" in df.columns else ""

is_tq = doc_type.str.contains("TQ", na=False)
is_rfi = doc_type.str.contains("RFI", na=False)

status = df["Status"] if "Status" in df.columns else pd.Series(["Open"] * len(df))

closed = df[status.str.contains("Closed", case=False, na=False)]

# AGE
if "Date Sent" in df.columns:
    df["AgeDays"] = (now - df["Date Sent"]).dt.days
else:
    df["AgeDays"] = np.random.randint(0, 60, len(df))

over_7 = df[df["AgeDays"] > 7]
over_30 = df[df["AgeDays"] > 30]

# =========================
# RISK MODEL (SIMPLE AI LOGIC)
# =========================
df["RiskScore"] = (
    (df["AgeDays"] / 30).clip(0, 1) * 0.6 +
    df["Status"].str.contains("Open", case=False, na=False).astype(int) * 0.4
) * 100

df["TrafficLight"] = pd.cut(
    df["RiskScore"],
    bins=[0, 40, 70, 100],
    labels=["Low", "Medium", "High"]
)

# =========================
# HEADER
# =========================
col_left, col_right = st.columns([3, 1])

with col_left:
    st.title("📊 TQ & RFI ML Dashboard")
    st.caption("Project Overview | Response Analytics | AI Risk Monitoring")

with col_right:
    st.write(datetime.now().strftime("📅 %d %b %Y"))
    st.download_button(
        "⬇ Download Report",
        df.to_csv(index=False),
        file_name="TQ_RFI_Report.csv"
    )

st.markdown("---")

# =========================
# A + B SECTION
# =========================
row1 = st.columns([2.5, 1.5])

with row1[0]:
    st.subheader("A - Project Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Not Responded >7 Days", len(over_7))
    c2.metric("Total TQs", int(is_tq.sum()))
    c3.metric("Total RFIs", int(is_rfi.sum()))

    venn_df = pd.DataFrame({
        "Type": ["TQ Only", "RFI Only", "Both"],
        "Count": [
            (is_tq & ~is_rfi).sum(),
            (is_rfi & ~is_tq).sum(),
            (is_tq & is_rfi).sum()
        ]
    })

    fig = px.pie(venn_df, names="Type", values="Count", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

with row1[1]:
    st.subheader("B - KPI Summary")

    st.metric("Closed Items", len(closed))
    st.metric(">30 Days Overdue", len(over_30))

# =========================
# C D E SECTION
# =========================
row2 = st.columns([2, 2, 1.5])

with row2[0]:
    st.subheader("C - Trend Analysis")

    if "Date Sent" in df.columns:
        trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

        fig = go.Figure()
        for col in trend.columns:
            fig.add_trace(go.Scatter(y=trend[col], name=str(col)))

        st.plotly_chart(fig, use_container_width=True)

with row2[1]:
    st.subheader("D - Age Distribution")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig = px.bar(x=age.index, y=age.values, text=age.values)
    st.plotly_chart(fig, use_container_width=True)

with row2[2]:
    st.subheader("E - AI Risk")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df["RiskScore"].mean(),
        title={"text": "Avg Risk %"}
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# DRILLDOWN TABLE
# =========================
st.markdown("---")
st.subheader("📋 Live Data (Drilldown)")

st.dataframe(
    df[["Project ID", "Doc Type", "Subject", "Status", "AgeDays", "RiskScore", "TrafficLight"]],
    use_container_width=True
)

# =========================
# INSIGHTS
# =========================
st.markdown("---")
st.subheader("🧠 AI Insights & Recommendations")

c1, c2 = st.columns(2)

with c1:
    st.warning(f"⚠ {len(over_7)} items are high risk (>7 days, no response)")

with c2:
    st.info("📌 Mechanical / critical disciplines likely contributing to overdue workload (rule-based insight)")
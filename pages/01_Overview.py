import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(page_title="Overview", layout="wide")

# =========================
# LOAD REAL DATA
# =========================
df = load_data()
m = get_metrics(df)

if df is None or df.empty:
    st.warning("No data available in Excel file.")
    st.stop()

# =========================
# CLEAN DATE HANDLING (REAL DATA ONLY)
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
df["Required Date"] = pd.to_datetime(df["Required Date"], errors="coerce", dayfirst=True)
df["Reply Date"] = pd.to_datetime(df["Reply Date"], errors="coerce", dayfirst=True)

today = pd.Timestamp.today().normalize()

df["AgeDays"] = (today - df["Date Sent"]).dt.days
df["IsOverdue"] = df["Reply Date"].isna() & (df["Required Date"] < today)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 📊 TQ & RFI Overview Dashboard")
    st.caption("Executive Summary – Live Project Communication Data")

with col2:
    st.markdown(f"### 📅 {datetime.today().strftime('%d %b %Y')}")

st.markdown("---")

# =========================
# KPI ROW (EXECUTIVE CARDS)
# =========================
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total TQ", m["total_tq"])
k2.metric("Total RFI", m["total_rfi"])
k3.metric("Closed", m["closed"])
k4.metric("Open", m["open"])
k5.metric("Overdue", m["overdue7"])
k6.metric("SLA %", f"{m['sla']}%")

st.markdown("---")

# =========================
# ROW 2: OVERVIEW + VENN STYLE INSIGHT
# =========================
c1, c2 = st.columns([2, 3])

with c1:
    st.markdown("### 📌 Project Health")

    overdue_tq = len(df[(df["Doc Type"] == "TQ") & (df["IsOverdue"])])
    overdue_rfi = len(df[(df["Doc Type"] == "RFI") & (df["IsOverdue"])])

    st.metric("TQ Overdue", overdue_tq)
    st.metric("RFI Overdue", overdue_rfi)

    st.info("Overdue is calculated using Required Date vs Reply Date")

with c2:
    st.markdown("### 🔵 Communication Flow")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[1,2,3], y=[1,2,3], mode="markers", marker_size=0))

    fig.add_annotation(x=1, y=2, text=f"TQ Overdue<br>{overdue_tq}", showarrow=False)
    fig.add_annotation(x=2, y=2, text=f"Overlap Risk<br>{min(overdue_tq, overdue_rfi)}", showarrow=False)
    fig.add_annotation(x=3, y=2, text=f"RFI Overdue<br>{overdue_rfi}", showarrow=False)

    fig.update_layout(
        template="plotly_dark",
        height=280,
        xaxis_visible=False,
        yaxis_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# ROW 3: TREND + AGEING
# =========================
c3, c4 = st.columns(2)

with c3:
    st.markdown("### 📈 Trend (TQ vs RFI)")

    trend = df.groupby(["Date Sent", "Doc Type"]).size().reset_index(name="Count")

    fig2 = px.line(
        trend,
        x="Date Sent",
        y="Count",
        color="Doc Type",
        markers=True
    )

    fig2.update_layout(template="plotly_dark", height=300)

    st.plotly_chart(fig2, use_container_width=True)

with c4:
    st.markdown("### ⏳ Age Distribution")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

    age = df.groupby("AgeBand").size().reset_index(name="Count")

    fig3 = px.bar(
        age,
        x="Count",
        y="AgeBand",
        orientation="h"
    )

    fig3.update_layout(template="plotly_dark", height=300)

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# =========================
# ROW 4: AI INSIGHTS (REAL DATA ONLY)
# =========================
c5, c6 = st.columns(2)

with c5:
    st.markdown("### 🧠 AI Insights (Rule-Based)")

    top_recipient = df["Recipient"].value_counts().idxmax()

    st.error(f"{m['overdue7']} items are overdue risk candidates")
    st.warning(f"{top_recipient} has highest workload pressure")

    if m["sla"] < 80:
        st.warning("SLA performance below target threshold (80%)")
    else:
        st.success("SLA performance within acceptable range")

with c6:
    st.markdown("### ⚠ Risk Indicator")

    risk = min(100, int((m["overdue7"] / max(1, m["open"])) * 100))

    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={"text": "Risk Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "green"},
                {"range": [40, 70], "color": "orange"},
                {"range": [70, 100], "color": "red"}
            ]
        }
    ))

    fig4.update_layout(template="plotly_dark", height=300)

    st.plotly_chart(fig4, use_container_width=True)
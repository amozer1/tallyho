import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_data
from utils.metrics import compute_metrics


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-testid="stMetric"] {
    border: 1px solid #2A3A4A;
    padding: 10px;
    border-radius: 10px;
    background-color: #0E1621;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# LOAD DATA
# -----------------------------
file = st.file_uploader("Upload Excel File", type=["xlsx"])

df = load_data(file) if file else load_data("data/TQ_TH.xlsx")

m = compute_metrics(df)


# -----------------------------
# KPI ROW
# -----------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("TQs", m["tq"])
c2.metric("RFIs", m["rfi"])
c3.metric("Open Items", m["open"])
c4.metric("Overdue >7d", m["overdue7"])
c5.metric("SLA %", m["sla"])


st.markdown("---")


# -----------------------------
# MAIN LAYOUT
# -----------------------------
left, right = st.columns([2, 1])


# =========================
# LEFT SIDE
# =========================
with left:

    st.subheader("📊 TQ vs RFI Overview")

    fig = px.pie(
        names=["TQ", "RFI"],
        values=[m["tq"], m["rfi"]],
        hole=0.6
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("📈 Communication Trend")

    trend = (
        m["df"]
        .groupby(m["df"]["Date Sent"].dt.date)["Doc Type"]
        .value_counts()
        .unstack()
        .fillna(0)
    )

    fig2 = go.Figure()

    if "TQ" in trend:
        fig2.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))

    if "RFI" in trend:
        fig2.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

    st.plotly_chart(fig2, use_container_width=True)


# =========================
# RIGHT SIDE
# =========================
with right:

    st.subheader("⏱ Ageing Profile")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    temp_df = m["df"].copy()
    temp_df["AgeBand"] = pd.cut(temp_df["AgeDays"], bins=bins, labels=labels)

    age_counts = temp_df["AgeBand"].value_counts().reindex(labels).fillna(0)

    st.bar_chart(age_counts)


    st.subheader("⚠ Risk Summary")

    st.metric("Overdue >7 days", m["overdue7"])
    st.metric("Overdue >30 days", m["overdue30"])
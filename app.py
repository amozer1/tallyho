import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    return df

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
df = load_data(uploaded_file) if uploaded_file else load_data("data/TQ_TH.xlsx")

# =========================
# CLEAN DATA
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())
df["AgeDays"] = (now - df["Date Sent"]).dt.days

df["Doc Type"] = df["Doc Type"].str.upper()

tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]
overdue_7 = df[df["AgeDays"] > 7]
overdue_30 = df[df["AgeDays"] > 30]

risk = round(len(overdue_7) / len(df) * 100, 1)

# =========================
# HEADER
# =========================
st.title("📊 TQ & RFI Executive Control Centre")
st.caption(f"Last refresh: {datetime.now().strftime('%d %b %Y %H:%M')}")

st.markdown("---")

# =========================
# KPI ROW (TOP CARDS)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Overdue >7 Days", len(overdue_7))
c2.metric("Total TQs", len(tq))
c3.metric("Total RFIs", len(rfi))
c4.metric("Risk Level (%)", risk)

st.markdown("---")

# =========================
# MAIN CONTROL GRID
# =========================
left, right = st.columns([2, 1])

# =========================
# LEFT SIDE (A + C + TABLE)
# =========================
with left:

    st.subheader("A - Overview: TQ vs RFI Split")

    pie = px.pie(
        names=["TQ", "RFI"],
        values=[len(tq), len(rfi)],
        hole=0.5
    )
    st.plotly_chart(pie, use_container_width=True)

    st.subheader("C - Trend (Created Items Over Time)")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig_trend = go.Figure()

    if "TQ" in trend.columns:
        fig_trend.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))
    if "RFI" in trend.columns:
        fig_trend.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("📋 Live Register")

    st.dataframe(
        df[[
            "Project ID",
            "Doc Type",
            "Seq No",
            "Sender",
            "Recipient",
            "Subject",
            "Status",
            "AgeDays"
        ]],
        use_container_width=True
    )

# =========================
# RIGHT SIDE (B + D + E)
# =========================
with right:

    st.subheader("B - Control Metrics")

    st.metric("Overdue >30 Days", len(overdue_30))
    st.metric("Open Items", len(df[df["Status"].str.upper() == "OPEN"]))

    st.markdown("---")

    st.subheader("D - Ageing Distribution")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    st.bar_chart(age)

    st.markdown("---")

    st.subheader("E - AI Risk Gauge")

    fig_risk = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        gauge={"axis": {"range": [0, 100]}},
        title={"text": "Delay Risk %"}
    ))

    st.plotly_chart(fig_risk, use_container_width=True)

# =========================
# FOOTER INSIGHTS
# =========================
st.markdown("---")

st.subheader("🧠 Executive Insights")

col1, col2 = st.columns(2)

col1.warning(f"{len(overdue_7)} items overdue (>7 days)")
col2.info(f"Highest workload sender: {df['Sender'].value_counts().idxmax()}")
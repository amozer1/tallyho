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

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(uploaded_file) if uploaded_file else load_data("data/TQ_TH.xlsx")

# =========================
# CLEAN
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
now = pd.Timestamp(datetime.now())

df["AgeDays"] = (now - df["Date Sent"]).dt.days

df["Doc Type"] = df["Doc Type"].str.upper()

tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]

overdue = df[df["AgeDays"] > 7]

risk = round(len(overdue) / len(df) * 100, 1)

# =========================
# FRAME STYLE FUNCTION
# =========================
def framed(title, content):
    st.markdown(f"""
    <div style="
        border:2px solid #1f2937;
        border-radius:10px;
        padding:10px;
        margin-bottom:15px;
        background:#0f172a;
        color:white;
    ">
        <h4 style="margin:0 0 10px 0;">{title}</h4>
    """, unsafe_allow_html=True)

    content()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 TQ & RFI EXECUTIVE CONTROL CENTRE")
st.caption(f"Live System | {datetime.now().strftime('%d %b %Y %H:%M')}")

st.markdown("---")

# =========================
# KPI ROW (FRAMED)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Overdue >7", len(overdue))
c2.metric("TQ", len(tq))
c3.metric("RFI", len(rfi))
c4.metric("Risk %", risk)

st.markdown("---")

# =========================
# MAIN GRID
# =========================
left, right = st.columns([2, 1])

# =========================
# LEFT SIDE
# =========================
with left:

    # PIE (A)
    def pie_block():
        fig = px.pie(
            names=["TQ", "RFI"],
            values=[len(tq), len(rfi)],
            hole=0.5
        )
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    framed("A - TQ vs RFI Overview", pie_block)

    # TREND (C)
    def trend_block():
        trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

        fig = go.Figure()
        if "TQ" in trend:
            fig.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))
        if "RFI" in trend:
            fig.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    framed("C - Trend Analysis", trend_block)

    # TABLE
    def table_block():
        st.dataframe(
            df[["Doc Type","Seq No","Sender","Recipient","Status","AgeDays"]],
            use_container_width=True
        )

    framed("📋 Live Register", table_block)

# =========================
# RIGHT SIDE
# =========================
with right:

    # B - KPIs
    def kpi_block():
        st.metric("Overdue >30", len(df[df["AgeDays"] > 30]))
        st.metric("Open Items", len(df[df["Status"].str.upper()=="OPEN"]))

    framed("B - Control KPIs", kpi_block)

    # D - AGEING
    def ageing_block():
        bins = [0,2,7,14,30,999]
        labels = ["0-2","3-7","8-14","15-30","30+"]

        df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
        age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

        fig = px.bar(x=age.index, y=age.values)
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    framed("D - Ageing Distribution", ageing_block)

    # E - RISK
    def risk_block():
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            gauge={"axis":{"range":[0,100]}}
        ))

        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    framed("E - AI Risk Engine", risk_block)

# =========================
# INSIGHTS
# =========================
st.markdown("---")

st.subheader("🧠 Executive Insights")

col1, col2 = st.columns(2)

col1.warning(f"{len(overdue)} items overdue (>7 days)")
col2.info(f"Top sender: {df['Sender'].value_counts().idxmax()}")
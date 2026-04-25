import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_venn_overview(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMNS
    # =========================
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["date sent", "reply date", "status", "doc type"]
    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # PARSE DATES
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())

    # =========================
    # AGE CALCULATION
    # =========================
    df["age_days"] = (today - df["date sent"]).dt.days

    # =========================
    # STATUS CLASSIFICATION
    # =========================
    def classify(row):

        # CLOSED RULE
        if pd.notna(row["reply date"]) or str(row["status"]).lower() == "closed":
            return "Closed"

        # OPEN / OUTSTANDING RULE
        if row["age_days"] <= 7:
            return "Open"
        else:
            return "Outstanding"

    df["state"] = df.apply(classify, axis=1)

    # =========================
    # SPLIT COUNTS
    # =========================
    open_count = len(df[df["state"] == "Open"])
    closed_count = len(df[df["state"] == "Closed"])
    outstanding_count = len(df[df["state"] == "Outstanding"])

    tq_count = len(df[df["doc type"] == "tq"])
    rfi_count = len(df[df["doc type"] == "rfi"])

    # =========================
    # TITLE
    # =========================
    st.markdown("## TQ & RFI Controls Tracker")

    # =========================
    # MAIN DONUT (STATUS VIEW)
    # =========================
    fig1 = go.Figure(data=[go.Pie(
        labels=["Open (≤7 days)", "Outstanding (>7 days)", "Closed"],
        values=[open_count, outstanding_count, closed_count],
        hole=0.65,
        marker=dict(colors=["#4da3ff", "#ff4d4d", "#22c55e"])
    )])

    fig1.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # SECONDARY BAR (TQ vs RFI)
    # =========================
    fig2 = go.Figure(data=[
        go.Bar(name="TQ", x=["TQ"], y=[tq_count], marker_color="#60a5fa"),
        go.Bar(name="RFI", x=["RFI"], y=[rfi_count], marker_color="#fbbf24")
    ])

    fig2.update_layout(
        barmode="group",
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title="TQ vs RFI Volume"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # KPI CARDS
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Open (≤7 days)", open_count)

    with col2:
        st.metric("Outstanding (>7 days)", outstanding_count)

    with col3:
        st.metric("Closed", closed_count)

    # =========================
    # INSIGHT BLOCK
    # =========================
    st.markdown("---")

    total = len(df)

    st.markdown(f"""
### Insight Summary

- Total Records: **{total}**
- Open Rate: **{round((open_count / total) * 100, 1)}%**
- Outstanding Rate: **{round((outstanding_count / total) * 100, 1)}%**
- Closure Rate: **{round((closed_count / total) * 100, 1)}%**

> Open = within 7 days of issue  
> Outstanding = older than 7 days without response  
> Closed = response received
""")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available for trend analysis.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # DATE HANDLING (YOUR DATA)
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    df["month_sent"] = df["date sent"].dt.to_period("M").dt.to_timestamp()
    df["month_closed"] = df["reply date"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # SPLIT TYPES
    # =========================
    rfi = df[df["doc type"] == "RFI"]
    tq = df[df["doc type"] == "TQ"]

    # =========================
    # SERIES BUILDER
    # =========================
    def build(data):

        raised = data.groupby("month_sent").size().reset_index(name="raised")

        closed = (
            data[data["status"].str.lower() == "closed"]
            .groupby("month_closed")
            .size()
            .reset_index(name="closed")
        )

        merged = pd.merge(
            raised,
            closed,
            left_on="month_sent",
            right_on="month_closed",
            how="outer"
        ).fillna(0)

        merged["month"] = merged["month_sent"].fillna(merged["month_closed"])
        merged["month"] = pd.to_datetime(merged["month"], errors="coerce")

        merged = merged.sort_values("month")

        merged["backlog"] = merged["raised"].cumsum() - merged["closed"].cumsum()

        return merged

    rfi_ts = build(rfi)
    tq_ts = build(tq)

    # =========================
    # SINGLE CLEAN FIGURE
    # =========================
    fig = go.Figure()

    # =========================
    # RFI (BLUE FAMILY)
    # =========================
    fig.add_trace(go.Scatter(
        x=rfi_ts["month"],
        y=rfi_ts["raised"],
        mode="lines+markers",
        name="RFI Raised",
        line=dict(color="#1f77b4", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=rfi_ts["month"],
        y=rfi_ts["closed"],
        mode="lines+markers",
        name="RFI Closed",
        line=dict(color="#6baed6", width=3)
    ))

    # =========================
    # TQ (GREEN FAMILY)
    # =========================
    fig.add_trace(go.Scatter(
        x=tq_ts["month"],
        y=tq_ts["raised"],
        mode="lines+markers",
        name="TQ Raised",
        line=dict(color="#2ca02c", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=tq_ts["month"],
        y=tq_ts["closed"],
        mode="lines+markers",
        name="TQ Closed",
        line=dict(color="#98df8a", width=3)
    ))

    # =========================
    # BACKLOG (ALL WORK)
    # =========================
    total = df.copy()
    total = build(total)

    fig.add_trace(go.Scatter(
        x=total["month"],
        y=total["backlog"],
        mode="lines",
        name="Total Backlog",
        line=dict(color="#ff7f0e", width=4, dash="dash")
    ))

    # =========================
    # LAYOUT (CLEAN EXECUTIVE STYLE)
    # =========================
    fig.update_layout(
        title="TQ / RFI Trend Overview",
        template="plotly_white",
        height=520,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
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
    # ONLY VALID TIME FIELD
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["month"] = df["date sent"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # ONLY VALID STATE FIELD
    # =========================
    df["is_closed"] = df["status"].str.lower().eq("closed")

    # =========================
    # SPLIT BY TYPE (EXISTING FIELD)
    # =========================
    rfi = df[df["doc type"] == "RFI"]
    tq = df[df["doc type"] == "TQ"]

    # =========================
    # PURE TRANSFORMATION (NO INVENTION)
    # =========================
    def build(data):

        # Raised = actual records in that month
        raised = data.groupby("month").size().reset_index(name="raised")

        # Closed = ONLY status-based filtering (no Reply Date used)
        closed = (
            data[data["is_closed"]]
            .groupby("month")
            .size()
            .reset_index(name="closed")
        )

        merged = pd.merge(raised, closed, on="month", how="outer").fillna(0)
        merged = merged.sort_values("month")

        # Backlog is mathematically derived (not assumed)
        merged["backlog"] = merged["raised"].cumsum() - merged["closed"].cumsum()

        return merged

    rfi_ts = build(rfi)
    tq_ts = build(tq)

    # =========================
    # SINGLE CLEAN GRAPH
    # =========================
    fig = go.Figure()

    # RFI
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
        line=dict(color="#6baed6", width=3, dash="dot")
    ))

    # TQ
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
        line=dict(color="#98df8a", width=3, dash="dot")
    ))

    # BACKLOG (DERIVED ONLY)
    total = df.groupby("month").size().reset_index(name="raised")

    total_closed = df[df["is_closed"]].groupby("month").size().reset_index(name="closed")

    total = pd.merge(total, total_closed, on="month", how="outer").fillna(0)
    total = total.sort_values("month")

    total["backlog"] = total["raised"].cumsum() - total["closed"].cumsum()

    fig.add_trace(go.Scatter(
        x=total["month"],
        y=total["backlog"],
        mode="lines",
        name="Backlog",
        line=dict(color="#ff7f0e", width=4, dash="dash")
    ))

    # =========================
    # CLEAN LAYOUT
    # =========================
    fig.update_layout(
        title="TQ / RFI Trend (Derived from Register Data Only)",
        template="plotly_white",
        height=520,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
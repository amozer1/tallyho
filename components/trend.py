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
    # SAFE DATE PARSING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")

    # REMOVE BAD ROWS (CRITICAL FIX)
    df = df[df["date sent"].notna()].copy()

    # =========================
    # CREATE MONTH (STRING - NOT DATETIME)
    # THIS IS THE KEY FIX
    # =========================
    df["month"] = df["date sent"].dt.to_period("M").astype(str)

    # =========================
    # STATE
    # =========================
    df["is_closed"] = df["status"].str.lower().eq("closed")

    # =========================
    # SPLIT TYPES
    # =========================
    tq = df[df["doc type"] == "TQ"]
    rfi = df[df["doc type"] == "RFI"]

    # =========================
    # BUILD SERIES (SAFE GROUPING)
    # =========================
    tq_created = tq.groupby("month").size().reset_index(name="tq_created")
    rfi_created = rfi.groupby("month").size().reset_index(name="rfi_created")
    closed = df[df["is_closed"]].groupby("month").size().reset_index(name="closed")

    # =========================
    # BUILD CONTROLLED AXIS (NO AUTO EXPANSION)
    # =========================
    all_months = pd.DataFrame({"month": sorted(df["month"].unique())})

    data = all_months.merge(tq_created, on="month", how="left")
    data = data.merge(rfi_created, on="month", how="left")
    data = data.merge(closed, on="month", how="left")

    data = data.fillna(0)

    # =========================
    # FORCE ORDER (CRITICAL)
    # =========================
    data = data.sort_values("month")

    # =========================
    # PLOT (3 CLEAN LINES)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["tq_created"],
        mode="lines+markers",
        name="TQs Created",
        line=dict(color="#2ca02c", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["rfi_created"],
        mode="lines+markers",
        name="RFIs Created",
        line=dict(color="#1f77b4", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["closed"],
        mode="lines+markers",
        name="Closed",
        line=dict(color="#ff7f0e", width=4)
    ))

    # =========================
    # HARD LOCK AXIS (PREVENTS FAKE DATES)
    # =========================
    fig.update_layout(
        title="TQ / RFI Trend (Strict Data Lock)",
        template="plotly_white",
        height=520,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        margin=dict(l=40, r=40, t=60, b=40),

        # 🔥 CRITICAL FIX
        xaxis=dict(
            type="category"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
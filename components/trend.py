import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # VALID DATE ONLY (YOUR DATA)
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df[df["date sent"].notna()].copy()

    df["month"] = df["date sent"].dt.to_period("M").astype(str)

    # =========================
    # STATE
    # =========================
    df["is_closed"] = df["status"].str.lower().eq("closed")

    # =========================
    # MONTHLY COUNTS
    # =========================
    monthly = df.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    if "RFI" not in monthly.columns:
        monthly["RFI"] = 0
    if "TQ" not in monthly.columns:
        monthly["TQ"] = 0

    monthly = monthly.reset_index().sort_values("month")

    closed = df[df["is_closed"]].groupby("month").size().reset_index(name="closed")

    data = monthly.merge(closed, on="month", how="left").fillna(0)

    # =========================
    # STACK LOGIC (TRUE 2D STACKED LINE)
    # =========================
    data["rfi_stack"] = data["RFI"]
    data["tq_stack"] = data["RFI"] + data["TQ"]
    data["closed_stack"] = data["RFI"] + data["TQ"] + data["closed"]

    # =========================
    # PLOT
    # =========================
    fig = go.Figure()

    # RFI base
    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["rfi_stack"],
        mode="lines+markers",
        name="RFI Created",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=7)
    ))

    # TQ stacked
    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["tq_stack"],
        mode="lines+markers",
        name="TQ Created (Stacked)",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=7)
    ))

    # Closed stacked
    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["closed_stack"],
        mode="lines+markers",
        name="Closed (Stacked)",
        line=dict(color="#ff7f0e", width=4),
        marker=dict(size=8)
    ))

    # =========================
    # CLEAN LAYOUT
    # =========================
    fig.update_layout(
        title="Stacked Line Chart (RFI / TQ / Closed)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        xaxis_title="Month",
        yaxis_title="Stacked Volume"
    )

    st.plotly_chart(fig, use_container_width=True)
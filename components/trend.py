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
    # STRICT DATE CLEANING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df[df["date sent"].notna()].copy()

    # REAL TIME AXIS (NO STRINGS)
    df["month"] = df["date sent"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # STATE
    # =========================
    df["is_closed"] = df["status"].str.lower().eq("closed")

    # =========================
    # AGGREGATION (REAL MONTHS ONLY)
    # =========================
    grouped = df.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    if "RFI" not in grouped.columns:
        grouped["RFI"] = 0
    if "TQ" not in grouped.columns:
        grouped["TQ"] = 0

    closed = df[df["is_closed"]].groupby("month").size()

    data = grouped.join(closed.rename("Closed"), how="outer").fillna(0)

    # IMPORTANT: enforce real ordering
    data = data.sort_index()

    # =========================
    # STACK LOGIC (VISUAL ONLY)
    # =========================
    data["RFI_stack"] = data["RFI"]
    data["TQ_stack"] = data["RFI"] + data["TQ"]
    data["Closed_stack"] = data["RFI"] + data["TQ"] + data["Closed"]

    # =========================
    # PLOT (REAL DATES ON X-AXIS)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["RFI_stack"],
        mode="lines+markers",
        name="RFI Created",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["TQ_stack"],
        mode="lines+markers",
        name="TQ Created",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Closed_stack"],
        mode="lines+markers",
        name="Closed",
        line=dict(color="#ff7f0e", width=4),
        marker=dict(size=8)
    ))

    # =========================
    # CRITICAL: FORCE REAL DATE AXIS
    # =========================
    fig.update_layout(
        title="Stacked Trend (Real Date Axis Only)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        xaxis=dict(
            title="Date Sent (Month)",
            type="date"   # 🔥 THIS IS THE KEY FIX
        ),
        yaxis_title="Volume"
    )

    st.plotly_chart(fig, use_container_width=True)
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
    # 🔥 FORCE UK DATE FORMAT (CRITICAL FIX)
    # =========================
    df["date sent"] = pd.to_datetime(
        df["date sent"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    df = df[df["date sent"].notna()].copy()

    # =========================
    # REAL TIME AXIS
    # =========================
    df["month"] = df["date sent"].dt.to_period("M").dt.to_timestamp()

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

    closed = df[df["is_closed"]].groupby("month").size()

    data = monthly.join(closed.rename("Closed"), how="outer").fillna(0)
    data = data.sort_index()

    # =========================
    # CUMULATIVE STACK (VALID VIEW)
    # =========================
    data["RFI_cum"] = data["RFI"].cumsum()
    data["TQ_cum"] = data["TQ"].cumsum()
    data["Closed_cum"] = data["Closed"].cumsum()

    data["stack_rfi"] = data["RFI_cum"]
    data["stack_tq"] = data["RFI_cum"] + data["TQ_cum"]
    data["stack_closed"] = data["RFI_cum"] + data["TQ_cum"] + data["Closed_cum"]

    # =========================
    # PLOT
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["stack_rfi"],
        mode="lines+markers",
        name="RFI (Cumulative)",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["stack_tq"],
        mode="lines+markers",
        name="TQ (Cumulative)",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["stack_closed"],
        mode="lines+markers",
        name="Closed (Cumulative)",
        line=dict(color="#ff7f0e", width=4),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title="Stacked Trend (Correct UK Date Handling)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        xaxis=dict(title="Date Sent", type="date"),
        yaxis_title="Cumulative Volume"
    )

    st.plotly_chart(fig, use_container_width=True)
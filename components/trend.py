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
    # REAL DATE PARSING (UK FORMAT FIXED)
    # =========================
    df["reply date"] = pd.to_datetime(
        df["reply date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # keep only valid dates
    df = df[df["reply date"].notna()].copy()

    # only CLOSED records
    df = df[df["status"].str.lower() == "closed"].copy()

    # =========================
    # REAL MONTH AXIS (NO STRINGS)
    # =========================
    df["month"] = df["reply date"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # GROUP BY REAL MONTHS
    # =========================
    grouped = df.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    if "RFI" not in grouped.columns:
        grouped["RFI"] = 0
    if "TQ" not in grouped.columns:
        grouped["TQ"] = 0

    # IMPORTANT: enforce correct time order
    grouped = grouped.sort_index()

    data = grouped.reset_index()

    # =========================
    # PLOT (REAL MONTHS ON X-AXIS)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["RFI"],
        mode="lines+markers",
        name="RFI Closed",
        line=dict(color="#1f77b4", width=4),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=data["month"],
        y=data["TQ"],
        mode="lines+markers",
        name="TQ Closed",
        line=dict(color="#2ca02c", width=4),
        marker=dict(size=8)
    ))

    # =========================
    # CLEAN LAYOUT (REAL MONTHS ON HORIZONTAL AXIS)
    # =========================
    fig.update_layout(
        title="Closed Trends (Real Monthly Timeline)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),

        xaxis=dict(
            title="Month (from real data)",
            type="date",          # 🔥 forces real chronological axis
            tickformat="%b %Y"
        ),

        yaxis=dict(
            title="Number of Closures"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
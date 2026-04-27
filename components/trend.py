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
    # SAFE DATE PARSING (UK FORMAT)
    # =========================
    df["reply date"] = pd.to_datetime(
        df["reply date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    df = df[df["reply date"].notna()].copy()

    # ONLY CLOSED ITEMS (flow of completions)
    df = df[df["status"].str.lower() == "closed"].copy()

    # =========================
    # REAL MONTH AXIS
    # =========================
    df["month"] = df["reply date"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # GROUP BY MONTH + TYPE
    # =========================
    grouped = df.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    if "RFI" not in grouped.columns:
        grouped["RFI"] = 0
    if "TQ" not in grouped.columns:
        grouped["TQ"] = 0

    grouped = grouped.sort_index().reset_index()

    # =========================
    # FLOW BALANCE (STACKED AREA STYLE)
    # =========================
    fig = go.Figure()

    # RFI area (base)
    fig.add_trace(go.Scatter(
        x=grouped["month"],
        y=grouped["RFI"],
        mode="lines",
        name="RFI Closed",
        line=dict(color="#1f77b4", width=2),
        fill="tozeroy"
    ))

    # TQ stacked on RFI (flow layer)
    fig.add_trace(go.Scatter(
        x=grouped["month"],
        y=grouped["RFI"] + grouped["TQ"],
        mode="lines",
        name="TQ Closed",
        line=dict(color="#2ca02c", width=2),
        fill="tonexty"
    ))

    # =========================
    # LAYOUT (CLEAN DASHBOARD STYLE)
    # =========================
    fig.update_layout(
        title="Closure Flow Balance (RFI vs TQ)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),

        xaxis=dict(
            title="Month (Actual Data)",
            type="date",
            tickformat="%b %Y"
        ),

        yaxis=dict(
            title="Closed Volume"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
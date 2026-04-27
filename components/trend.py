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
    # REAL CLOSURE DATE
    # =========================
    df["reply date"] = pd.to_datetime(
        df["reply date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    df = df[df["reply date"].notna()].copy()
    df = df[df["status"].str.lower() == "closed"].copy()

    # =========================
    # REAL MONTH AXIS
    # =========================
    df["month"] = df["reply date"].dt.to_period("M").dt.to_timestamp()

    # =========================
    # GROUP
    # =========================
    grouped = df.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    if "RFI" not in grouped.columns:
        grouped["RFI"] = 0
    if "TQ" not in grouped.columns:
        grouped["TQ"] = 0

    grouped = grouped.sort_index().reset_index()

    # =========================
    # PLOT (CLEAR COMPARISON STYLE)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grouped["month"],
        y=grouped["RFI"],
        name="RFI Closed",
        marker=dict(color="#1f77b4")
    ))

    fig.add_trace(go.Bar(
        x=grouped["month"],
        y=grouped["TQ"],
        name="TQ Closed",
        marker=dict(color="#2ca02c")
    ))

    # =========================
    # OVERLAY MARKERS (OPTIONAL CLARITY BOOST)
    # =========================
    fig.add_trace(go.Scatter(
        x=grouped["month"],
        y=grouped["RFI"],
        mode="markers",
        name="RFI Points",
        marker=dict(color="#1f77b4", size=7),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=grouped["month"],
        y=grouped["TQ"],
        mode="markers",
        name="TQ Points",
        marker=dict(color="#2ca02c", size=7),
        showlegend=False
    ))

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        title="Monthly Closures (RFI vs TQ)",
        template="plotly_white",
        barmode="group",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02),
        xaxis=dict(
            title="Month",
            type="date",
            tickformat="%b %Y"
        ),
        yaxis=dict(title="Closed Count")
    )

    st.plotly_chart(fig, use_container_width=True)
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
    # CLEAN DATES (STRICT UK FORMAT)
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], format="%d/%m/%Y", errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], format="%d/%m/%Y", errors="coerce")

    # =========================
    # CREATED (FROM DATE SENT)
    # =========================
    created = df.dropna(subset=["date sent"]).copy()
    created["month"] = created["date sent"].dt.to_period("M").dt.to_timestamp()

    created_grouped = created.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    # =========================
    # CLOSED (FROM REPLY DATE)
    # =========================
    closed = df[df["status"].str.lower() == "closed"].dropna(subset=["reply date"]).copy()
    closed["month"] = closed["reply date"].dt.to_period("M").dt.to_timestamp()

    closed_grouped = closed.groupby(["month", "doc type"]).size().unstack(fill_value=0)

    # =========================
    # ALIGN DATA (REAL MONTHS ONLY)
    # =========================
    all_months = sorted(set(created_grouped.index) | set(closed_grouped.index))

    created_grouped = created_grouped.reindex(all_months, fill_value=0)
    closed_grouped = closed_grouped.reindex(all_months, fill_value=0)

    # ensure columns exist
    for col in ["RFI", "TQ"]:
        if col not in created_grouped.columns:
            created_grouped[col] = 0
        if col not in closed_grouped.columns:
            closed_grouped[col] = 0

    # =========================
    # PLOT (PROFESSIONAL MEETING STYLE)
    # =========================
    fig = go.Figure()

    # RFI created
    fig.add_trace(go.Scatter(
        x=all_months,
        y=created_grouped["RFI"],
        mode="lines+markers",
        name="RFI Created",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=7)
    ))

    # RFI closed
    fig.add_trace(go.Scatter(
        x=all_months,
        y=closed_grouped["RFI"],
        mode="lines+markers",
        name="RFI Closed",
        line=dict(color="#1f77b4", width=2, dash="dash"),
        marker=dict(size=6)
    ))

    # TQ created
    fig.add_trace(go.Scatter(
        x=all_months,
        y=created_grouped["TQ"],
        mode="lines+markers",
        name="TQ Created",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=7)
    ))

    # TQ closed
    fig.add_trace(go.Scatter(
        x=all_months,
        y=closed_grouped["TQ"],
        mode="lines+markers",
        name="TQ Closed",
        line=dict(color="#2ca02c", width=2, dash="dash"),
        marker=dict(size=6)
    ))

    # =========================
    # LAYOUT (CLEAN EXECUTIVE STYLE)
    # =========================
    fig.update_layout(
        title="RFI / TQ Flow (Created vs Closed)",
        template="plotly_white",
        height=520,
        hovermode="x unified",

        legend=dict(
            orientation="h",
            y=1.02
        ),

        xaxis=dict(
            title="Month",
            type="date",
            tickformat="%b %Y"
        ),

        yaxis=dict(
            title="Count"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
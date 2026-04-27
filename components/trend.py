import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):
    """
    Trend chart for:
    - Raised TQs
    - Raised RFIs
    - Closed TQs
    - Closed RFIs
    - Backlog
    """

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # -----------------------------
    # Clean columns
    # -----------------------------
    df.columns = df.columns.str.strip().str.lower()

    required_cols = ["doc type", "date sent", "reply date", "status"]

    for col in required_cols:
        if col not in df.columns:
            st.warning(f"Missing column: {col}")
            return

    # -----------------------------
    # Convert dates
    # -----------------------------
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce", dayfirst=True)
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce", dayfirst=True)

    df = df.dropna(subset=["date sent"])

    # -----------------------------
    # Raised trends
    # -----------------------------
    raised = (
        df.groupby([pd.Grouper(key="date sent", freq="W"), "doc type"])
        .size()
        .reset_index(name="count")
    )

    raised_pivot = raised.pivot(index="date sent", columns="doc type", values="count").fillna(0)

    # -----------------------------
    # Closed trends
    # -----------------------------
    closed_df = df.dropna(subset=["reply date"]).copy()

    closed = (
        closed_df.groupby([pd.Grouper(key="reply date", freq="W"), "doc type"])
        .size()
        .reset_index(name="count")
    )

    closed_pivot = closed.pivot(index="reply date", columns="doc type", values="count").fillna(0)

    # -----------------------------
    # Align indexes
    # -----------------------------
    all_dates = raised_pivot.index.union(closed_pivot.index)

    raised_pivot = raised_pivot.reindex(all_dates, fill_value=0)
    closed_pivot = closed_pivot.reindex(all_dates, fill_value=0)

    # -----------------------------
    # Backlog calculation
    # -----------------------------
    total_raised = raised_pivot.sum(axis=1)
    total_closed = closed_pivot.sum(axis=1)

    backlog = (total_raised - total_closed).cumsum()

    # -----------------------------
    # Build figure
    # -----------------------------
    fig = go.Figure()

    # Raised
    if "TQ" in raised_pivot.columns:
        fig.add_trace(go.Bar(
            x=raised_pivot.index,
            y=raised_pivot["TQ"],
            name="TQ Raised"
        ))

    if "RFI" in raised_pivot.columns:
        fig.add_trace(go.Bar(
            x=raised_pivot.index,
            y=raised_pivot["RFI"],
            name="RFI Raised"
        ))

    # Closed
    if "TQ" in closed_pivot.columns:
        fig.add_trace(go.Scatter(
            x=closed_pivot.index,
            y=closed_pivot["TQ"],
            mode="lines+markers",
            name="TQ Closed",
            line=dict(width=3)
        ))

    if "RFI" in closed_pivot.columns:
        fig.add_trace(go.Scatter(
            x=closed_pivot.index,
            y=closed_pivot["RFI"],
            mode="lines+markers",
            name="RFI Closed",
            line=dict(width=3)
        ))

    # Backlog
    fig.add_trace(go.Scatter(
        x=backlog.index,
        y=backlog,
        mode="lines",
        name="Backlog",
        yaxis="y2",
        line=dict(width=4, dash="dot")
    ))

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        title="TQ / RFI Trend Analysis",
        barmode="group",
        height=550,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            title="Week",
            showgrid=False
        ),
        yaxis=dict(
            title="Raised / Closed",
            showgrid=True
        ),
        yaxis2=dict(
            title="Backlog",
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)
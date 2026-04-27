import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if "date sent" not in df.columns or "reply date" not in df.columns:
        st.warning("Required columns missing.")
        return

    # -----------------------------
    # Convert dates
    # -----------------------------
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce", dayfirst=True)
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce", dayfirst=True)

    df = df.dropna(subset=["date sent"])

    # -----------------------------
    # Weekly raised
    # -----------------------------
    raised = (
        df.groupby(pd.Grouper(key="date sent", freq="W"))
        .size()
        .rename("raised")
    )

    # -----------------------------
    # Weekly closed
    # -----------------------------
    closed = (
        df.dropna(subset=["reply date"])
        .groupby(pd.Grouper(key="reply date", freq="W"))
        .size()
        .rename("closed")
    )

    # -----------------------------
    # Combine
    # -----------------------------
    trend = pd.concat([raised, closed], axis=1).fillna(0)

    trend["backlog"] = (trend["raised"] - trend["closed"]).cumsum()

    # -----------------------------
    # Plot
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend.index,
        y=trend["backlog"],
        mode="lines+markers",
        name="Open Backlog",
        line=dict(width=4),
        fill="tozeroy"
    ))

    fig.update_layout(
        title="Open Backlog Trend",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(
            title="Week",
            showgrid=False
        ),
        yaxis=dict(
            title="Open Items",
            showgrid=True
        )
    )

    st.plotly_chart(fig, use_container_width=True)
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    required_cols = ["date sent", "status"]

    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return

    # =========================
    # CLEAN DATES
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")

    # drop invalid dates
    df = df.dropna(subset=["date sent"])

    # =========================
    # SAFE STATUS HANDLING
    # =========================
    df["status"] = df["status"].fillna("").str.lower()

    df["is_open"] = df["status"].eq("open")
    df["is_closed"] = df["status"].eq("closed")

    # =========================
    # SORT FOR TIME SERIES
    # =========================
    df_sorted = df.sort_values("date sent")

    # cumulative counts
    df_sorted["open_cum"] = df_sorted["is_open"].cumsum()
    df_sorted["closed_cum"] = df_sorted["is_closed"].cumsum()

    # =========================
    # PLOT
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["open_cum"],
        mode="lines+markers",
        name="Open Items"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["closed_cum"],
        mode="lines+markers",
        name="Closed Items"
    ))

    fig.update_layout(
        title="RFI / TQ Workflow Trend",
        xaxis_title="Date Sent",
        yaxis_title="Cumulative Count",
        template="plotly_white",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # KPIs
    # =========================
    col1, col2, col3 = st.columns(3)

    total = len(df)
    open_count = df["is_open"].sum()
    closed_count = df["is_closed"].sum()

    col1.metric("Total Items", int(total))
    col2.metric("Open", int(open_count))
    col3.metric("Closed", int(closed_count))
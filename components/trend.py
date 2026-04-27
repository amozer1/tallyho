import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # CLEAN DATES
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    # =========================
    # CREATE STATUS FLAGS
    # =========================
    df["is_open"] = df["status"].str.lower().eq("open")
    df["is_closed"] = df["status"].str.lower().eq("closed")

    # =========================
    # TIME SERIES BUILD
    # =========================
    df_sorted = df.sort_values("date sent")

    df_sorted["open_cum"] = df_sorted["is_open"].cumsum()
    df_sorted["closed_cum"] = df_sorted["is_closed"].cumsum()

    # =========================
    # LINE CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["open_cum"],
        mode="lines",
        name="Open Items"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["date sent"],
        y=df_sorted["closed_cum"],
        mode="lines",
        name="Closed Items"
    ))

    fig.update_layout(
        title="RFI / TQ Workflow Trend",
        xaxis_title="Date Sent",
        yaxis_title="Cumulative Count",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # SIMPLE KPIs
    # =========================
    col1, col2, col3 = st.columns(3)

    total = len(df)
    open_count = df["is_open"].sum()
    closed_count = df["is_closed"].sum()

    col1.metric("Total Items", total)
    col2.metric("Open", open_count)
    col3.metric("Closed", closed_count)
import streamlit as st
import pandas as pd
import plotly.express as px


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # CLEAN DATES
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], format="%d/%m/%Y", errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], format="%d/%m/%Y", errors="coerce")

    df = df.dropna(subset=["date sent", "reply date"]).copy()

    # =========================
    # CYCLE TIME (REAL PERFORMANCE METRIC)
    # =========================
    df["cycle_days"] = (df["reply date"] - df["date sent"]).dt.days

    # keep only closed items (true completion cycles)
    df = df[df["status"].str.lower() == "closed"]

    # =========================
    # PLOT
    # =========================
    fig = px.box(
        df,
        x="doc type",
        y="cycle_days",
        color="doc type",
        points="all",
        title="RFI vs TQ Closure Time (Cycle Duration in Days)"
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        showlegend=False,
        xaxis_title="Document Type",
        yaxis_title="Days to Close"
    )

    st.plotly_chart(fig, use_container_width=True)
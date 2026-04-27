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
    # CLEAN DATES (REAL ONLY)
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], format="%d/%m/%Y", errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], format="%d/%m/%Y", errors="coerce")

    # =========================
    # CREATED
    # =========================
    created = df.dropna(subset=["date sent"]).copy()
    created["month"] = created["date sent"].dt.to_period("M").dt.to_timestamp()

    created_counts = created.groupby(["month", "doc type"]).size().unstack(fill_value=0)
    created_counts.columns = [f"{c} Created" for c in created_counts.columns]

    # =========================
    # CLOSED
    # =========================
    closed = df[df["status"].str.lower() == "closed"].dropna(subset=["reply date"]).copy()
    closed["month"] = closed["reply date"].dt.to_period("M").dt.to_timestamp()

    closed_counts = closed.groupby(["month", "doc type"]).size().unstack(fill_value=0)
    closed_counts.columns = [f"{c} Closed" for c in closed_counts.columns]

    # =========================
    # MERGE ALL
    # =========================
    data = created_counts.join(closed_counts, how="outer").fillna(0)
    data = data.sort_index().reset_index()
    data["month"] = data["month"].dt.strftime("%b %Y")

    # reshape for heatmap
    melted = data.melt(id_vars="month", var_name="Metric", value_name="Count")

    # =========================
    # HEATMAP (MEETING FRIENDLY)
    # =========================
    fig = px.density_heatmap(
        melted,
        x="Metric",
        y="month",
        z="Count",
        text_auto=True,
        color_continuous_scale="Blues",
        title="RFI / TQ Monthly Flow Snapshot"
    )

    fig.update_layout(
        template="plotly_white",
        height=520,
        xaxis_title="",
        yaxis_title="Month"
    )

    st.plotly_chart(fig, use_container_width=True)
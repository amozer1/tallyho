import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_by_age(df):

    if df is None or df.empty:
        st.warning("No data available")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")

    df["age"] = (pd.Timestamp.today().normalize() - df["date sent"]).dt.days
    df["age"] = df["age"].fillna(0)

    # =========================
    # AGE BANDS
    # =========================
    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2 days", "3–7 days", "8–14 days", "15–30 days", ">30 days"]

    df["age_band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df.groupby("age_band").size().reindex(labels, fill_value=0)

    total = len(df)

    # percentages
    pct = (summary / total * 100).round(1)

    # =========================
    # HEADER
    # =========================
    st.markdown("### 📊 Outstanding by Age")
    st.caption("Distribution of open TQs and RFIs by time outstanding")

    # =========================
    # CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary.values,
        y=summary.index,
        orientation="h",
        text=[f"{v} ({p}%)" for v, p in zip(summary.values, pct)],
        textposition="outside",
        marker=dict(color="#ef4444")
    ))

    fig.update_layout(
        height=400,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="Number of Items"),
        yaxis=dict(title="")
    )

    st.plotly_chart(fig, use_container_width=True)
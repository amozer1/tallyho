import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_age_outstanding(df):

    if df is None or df.empty:
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    today = pd.Timestamp.today()

    df["age"] = (today - df["date sent"]).dt.days

    # =========================
    # BUCKETS
    # =========================
    b1 = len(df[df["age"] <= 7])
    b2 = len(df[(df["age"] > 7) & (df["age"] <= 14)])
    b3 = len(df[df["age"] > 14])

    # =========================
    # HEADER (MATCH OUTSTANDING)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border-radius:10px;
        padding:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:#38bdf8;
        margin-bottom:6px;
    ">
        📊 Outstanding by Age
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI STYLE ROW (CONSISTENT)
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("0–7 Days", b1)
    col2.metric("7–14 Days", b2)
    col3.metric("14+ Days", b3)

    # =========================
    # CHART (SAME HEIGHT AS OUTSTANDING)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[b1, b2, b3],
        y=["0–7", "7–14", "14+"],
        orientation="h",
        marker=dict(color=["#22c55e", "#facc15", "#ef4444"])
    ))

    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)
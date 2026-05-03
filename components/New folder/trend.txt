import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_trend(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMNS
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    if "date sent" not in df.columns or "status" not in df.columns:
        st.error("Missing required columns: date sent / status")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df = df.dropna(subset=["date sent"])

    df["status"] = df["status"].astype(str).str.strip().str.upper()

    today = pd.Timestamp.today()

    # =========================
    # OPEN / CLOSED SPLIT
    # =========================
    open_df = df[df["status"] == "OPEN"]
    closed_df = df[df["status"] == "CLOSED"]

    total = len(df)
    open_count = len(open_df)
    closed_count = len(closed_df)

    open_pct = round((open_count / total) * 100, 1) if total else 0

    # =========================
    # SIMPLE TREND (DAILY COUNTS)
    # =========================
    df_sorted = df.sort_values("date sent")

    trend = df_sorted.groupby("date sent").size().cumsum().reset_index()
    trend.columns = ["date", "cumulative"]

    # =========================
    # STATUS HEADER (LIKE YOUR STYLE)
    # =========================
    if open_count > closed_count:
        color = "#f97316"
        status = "WORK IN PROGRESS"
    else:
        color = "#22c55e"
        status = "CONTROLLED"

    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:6px 10px;
        margin-bottom:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:{color};
    ">
        📊 RFI / TQ Trend — {status}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI ROW
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Open Items",
            value=open_count,
            delta=f"{open_pct}% of total"
        )

    with col2:
        st.metric(
            label="Closed Items",
            value=closed_count
        )

    # =========================
    # MINI TREND CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["date"],
        y=trend["cumulative"],
        mode="lines+markers",
        name="Cumulative Flow",
        line=dict(color=color)
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=11),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # FOOTER INSIGHT
    # =========================
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:2px;
    ">
        Open backlog at <span style="color:{color}; font-weight:600;">{open_pct}%</span> of total workload
    </div>
    """, unsafe_allow_html=True)
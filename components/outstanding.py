import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    status_col = "status"
    doc_col = "doc type"

    df[status_col] = df[status_col].astype(str).str.upper()
    df[doc_col] = df[doc_col].astype(str).str.upper()

    today = pd.Timestamp.today()

    open_df = df[df[status_col] == "OPEN"]
    overdue_df = open_df.copy()

    date_col = "date sent"
    overdue_df[date_col] = pd.to_datetime(overdue_df[date_col], errors="coerce")

    overdue_df = overdue_df[(today - overdue_df[date_col]).dt.days > 7]

    overdue_tq = len(overdue_df[overdue_df[doc_col] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df[doc_col] == "RFI"])

    # =========================
    # HEADER (SAME STYLE)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border-radius:10px;
        padding:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:#f97316;
        margin-bottom:6px;
    ">
        🚨 Outstanding (>7 Days)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI ROW (MINIMAL)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Overdue Items", len(overdue_df))

    with col2:
        st.metric("Total Open", len(open_df))

    # =========================
    # CHART (FORCED HEIGHT)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ", "RFI"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"])
    ))

    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)
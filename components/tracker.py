import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:8px 10px;
        margin-bottom:8px;
        text-align:center;
        font-size:13px;
        font-weight:800;
        color:#E2E8F0;
    ">
        📊 TQ & RFI Overview
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    # =========================
    # FIXED CIRCLE SYSTEM (NO OVERFLOW)
    # =========================

    # LEFT - TQ
    fig.add_shape(
        type="circle",
        x0=0.1, y0=0.35, x1=1.1, y1=1.35,
        fillcolor="rgba(59,130,246,0.18)",
        line=dict(color="#60A5FA", width=2)
    )

    # MIDDLE - TOTAL (BRIGHT BLUE)
    fig.add_shape(
        type="circle",
        x0=0.95, y0=0.25, x1=1.95, y1=1.45,
        fillcolor="rgba(0,123,255,0.25)",
        line=dict(color="#007BFF", width=3)
    )

    # RIGHT - RFI
    fig.add_shape(
        type="circle",
        x0=1.8, y0=0.35, x1=2.8, y1=1.35,
        fillcolor="rgba(34,197,94,0.18)",
        line=dict(color="#4ADE80", width=2)
    )

    # =========================
    # EXACT CENTERS (ANCHOR POINTS)
    # =========================
    tq_x, tq_y = 0.6, 0.85
    total_x, total_y = 1.45, 0.85
    rfi_x, rfi_y = 2.3, 0.85

    # =========================
    # TQ
    # =========================
    fig.add_annotation(
        x=tq_x, y=tq_y + 0.18,
        text="<b>TQ</b>",
        showarrow=False,
        font=dict(color="#60A5FA", size=13)
    )

    fig.add_annotation(
        x=tq_x, y=tq_y,
        text=f"<b style='font-size:26px'>{tq_total}</b>",
        showarrow=False,
        font=dict(color="white")
    )

    fig.add_annotation(
        x=tq_x, y=tq_y - 0.18,
        text=f"{tq_pct}% of total",
        showarrow=False,
        font=dict(color="rgba(255,255,255,0.75)", size=10)
    )

    # =========================
    # TOTAL (CENTRE FOCUS)
    # =========================
    fig.add_annotation(
        x=total_x, y=total_y + 0.18,
        text="<b>TOTAL</b>",
        showarrow=False,
        font=dict(color="#007BFF", size=13)
    )

    fig.add_annotation(
        x=total_x, y=total_y,
        text=f"<b style='font-size:30px'>{total}</b>",
        showarrow=False,
        font=dict(color="white")
    )

    fig.add_annotation(
        x=total_x, y=total_y - 0.18,
        text="All RFIs + TQs",
        showarrow=False,
        font=dict(color="rgba(255,255,255,0.75)", size=10)
    )

    # =========================
    # RFI
    # =========================
    fig.add_annotation(
        x=rfi_x, y=rfi_y + 0.18,
        text="<b>RFI</b>",
        showarrow=False,
        font=dict(color="#4ADE80", size=13)
    )

    fig.add_annotation(
        x=rfi_x, y=rfi_y,
        text=f"<b style='font-size:26px'>{rfi_total}</b>",
        showarrow=False,
        font=dict(color="white")
    )

    fig.add_annotation(
        x=rfi_x, y=rfi_y - 0.18,
        text=f"{rfi_pct}% of total",
        showarrow=False,
        font=dict(color="rgba(255,255,255,0.75)", size=10)
    )

    # =========================
    # STABLE LAYOUT (NO RESPONSIVE BREAKING)
    # =========================
    fig.update_layout(
        height=240,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[0, 3.0], fixedrange=True),
        yaxis=dict(visible=False, range=[0.2, 1.5], fixedrange=True)
    )

    st.plotly_chart(fig, use_container_width=True)
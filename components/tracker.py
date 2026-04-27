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
    df["age"] = (today - df["date sent"]).dt.days

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
        📊 Document Flow Overview
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    # =========================
    # CIRCLES (balanced sizing)
    # =========================

    # LEFT - TQ (blue)
    fig.add_shape(
        type="circle",
        x0=0.1, y0=0.35, x1=0.95, y1=1.2,
        fillcolor="rgba(59,130,246,0.18)",
        line=dict(color="#60A5FA", width=2)
    )

    # MIDDLE - TOTAL (BRIGHT BLUE FOCUS)
    fig.add_shape(
        type="circle",
        x0=1.05, y0=0.25, x1=1.95, y1=1.3,
        fillcolor="rgba(0,123,255,0.25)",
        line=dict(color="#007BFF", width=3)
    )

    # RIGHT - RFI (green)
    fig.add_shape(
        type="circle",
        x0=2.05, y0=0.35, x1=2.95, y1=1.2,
        fillcolor="rgba(34,197,94,0.18)",
        line=dict(color="#4ADE80", width=2)
    )

    # =========================
    # LEFT - TQ
    # =========================
    fig.add_annotation(x=0.52, y=0.88,
                       text="<b>TQs Only</b>",
                       showarrow=False,
                       font=dict(color="#60A5FA", size=13))

    fig.add_annotation(x=0.52, y=0.70,
                       text=f"<b style='font-size:26px'>{tq_total}</b>",
                       showarrow=False,
                       font=dict(color="white"))

    fig.add_annotation(x=0.52, y=0.52,
                       text=f"{tq_pct}% of workload",
                       showarrow=False,
                       font=dict(color="rgba(255,255,255,0.75)", size=10))

    fig.add_annotation(x=0.52, y=0.35,
                       text=f"{tq_not} pending",
                       showarrow=False,
                       font=dict(color="#60A5FA", size=10))

    # =========================
    # MIDDLE - TOTAL (FOCUS)
    # =========================
    fig.add_annotation(x=1.5, y=0.88,
                       text="<b>Total Workload</b>",
                       showarrow=False,
                       font=dict(color="#007BFF", size=13))

    fig.add_annotation(x=1.5, y=0.70,
                       text=f"<b style='font-size:30px'>{total}</b>",
                       showarrow=False,
                       font=dict(color="white"))

    fig.add_annotation(x=1.5, y=0.52,
                       text="All Documents",
                       showarrow=False,
                       font=dict(color="rgba(255,255,255,0.75)", size=10))

    fig.add_annotation(x=1.5, y=0.35,
                       text=f"{total_not} outstanding",
                       showarrow=False,
                       font=dict(color="#F87171", size=10))

    # =========================
    # RIGHT - RFI
    # =========================
    fig.add_annotation(x=2.48, y=0.88,
                       text="<b>RFIs Only</b>",
                       showarrow=False,
                       font=dict(color="#4ADE80", size=13))

    fig.add_annotation(x=2.48, y=0.70,
                       text=f"<b style='font-size:26px'>{rfi_total}</b>",
                       showarrow=False,
                       font=dict(color="white"))

    fig.add_annotation(x=2.48, y=0.52,
                       text=f"{rfi_pct}% of workload",
                       showarrow=False,
                       font=dict(color="rgba(255,255,255,0.75)", size=10))

    fig.add_annotation(x=2.48, y=0.35,
                       text=f"{rfi_not} pending",
                       showarrow=False,
                       font=dict(color="#4ADE80", size=10))

    # =========================
    # LAYOUT (IMPORTANT)
    # =========================
    fig.update_layout(
        height=220,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.1, 3.0]),
        yaxis=dict(visible=False, range=[0.0, 1.5])
    )

    st.plotly_chart(fig, use_container_width=True)
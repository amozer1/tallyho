import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    # =========================
    # VALIDATION
    # =========================
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

    # =========================
    # CLEAN DATA
    # =========================
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
        color:white;
    ">
        📊 TQ & RFI Status Overview
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    # =========================
    # CIRCLES
    # =========================

    fig.add_shape(
        type="circle",
        x0=0.0, y0=0.2,
        x1=1.2, y1=1.4,
        fillcolor="rgba(96,165,250,0.35)",
        line=dict(color="#60A5FA", width=2)
    )

    fig.add_shape(
        type="circle",
        x0=0.85, y0=0.15,
        x1=2.35, y1=1.65,
        fillcolor="rgba(168,85,247,0.45)",
        line=dict(color="#A855F7", width=2)
    )

    fig.add_shape(
        type="circle",
        x0=2.0, y0=0.2,
        x1=3.2, y1=1.4,
        fillcolor="rgba(74,222,128,0.35)",
        line=dict(color="#4ADE80", width=2)
    )

    # =========================
    # TRUE CENTER CALCULATIONS
    # =========================
    tq_x = (0.0 + 1.2) / 2
    tq_y = (0.2 + 1.4) / 2

    total_x = (0.85 + 2.35) / 2
    total_y = (0.15 + 1.65) / 2

    rfi_x = (2.0 + 3.2) / 2
    rfi_y = (0.2 + 1.4) / 2

    # =========================
    # TQ CENTERED BLOCK
    # =========================
    fig.add_annotation(
        x=tq_x, y=tq_y,
        text=f"<b>TQ</b><br><span style='font-size:26px'>{tq_total}</span><br><span style='font-size:11px'>{tq_pct}%</span>",
        showarrow=False,
        font=dict(color="#60A5FA"),
        align="center"
    )

    # =========================
    # TOTAL CENTERED BLOCK
    # =========================
    fig.add_annotation(
        x=total_x, y=total_y,
        text=f"<b>TOTAL</b><br><span style='font-size:30px'>{total}</span><br><span style='font-size:11px'>All Docs</span>",
        showarrow=False,
        font=dict(color="#A855F7"),
        align="center"
    )

    # =========================
    # RFI CENTERED BLOCK
    # =========================
    fig.add_annotation(
        x=rfi_x, y=rfi_y,
        text=f"<b>RFI</b><br><span style='font-size:26px'>{rfi_total}</span><br><span style='font-size:11px'>{rfi_pct}%</span>",
        showarrow=False,
        font=dict(color="#4ADE80"),
        align="center"
    )

    # =========================
    # NOT RESPONDED (SMALL FOOT NOTE INSIDE SAME SPACE)
    # =========================

    fig.add_annotation(x=tq_x, y=0.28,
                       text=f"{tq_not} not responded",
                       showarrow=False,
                       font=dict(color="#60A5FA", size=10))

    fig.add_annotation(x=total_x, y=0.28,
                       text=f"{total_not} not responded",
                       showarrow=False,
                       font=dict(color="#F87171", size=10))

    fig.add_annotation(x=rfi_x, y=0.28,
                       text=f"{rfi_not} not responded",
                       showarrow=False,
                       font=dict(color="#4ADE80", size=10))

    # =========================
    # LAYOUT
    # =========================

    fig.update_layout(
        height=420,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.3, 3.6]),
        yaxis=dict(visible=False, range=[-0.3, 2.0])
    )

    st.plotly_chart(fig, use_container_width=True)
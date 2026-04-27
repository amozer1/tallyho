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

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:8px;
        text-align:center;
        font-weight:800;
        color:#E2E8F0;
        margin-bottom:10px;
    ">
        📊 TQ & RFI Overview
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    # =========================
    # CIRCLES
    # =========================

    # TQ
    fig.add_shape(type="circle",
        x0=0.1, y0=0.3, x1=1.1, y1=1.3,
        fillcolor="rgba(59,130,246,0.18)",
        line=dict(color="#60A5FA", width=2)
    )

    # TOTAL (PURPLE FOCUS)
    fig.add_shape(type="circle",
        x0=0.95, y0=0.2, x1=1.95, y1=1.4,
        fillcolor="rgba(168,85,247,0.22)",
        line=dict(color="#A855F7", width=3)
    )

    # RFI
    fig.add_shape(type="circle",
        x0=1.8, y0=0.3, x1=2.8, y1=1.3,
        fillcolor="rgba(34,197,94,0.18)",
        line=dict(color="#4ADE80", width=2)
    )

    # =========================
    # CENTERS
    # =========================
    tq_x, tq_y = 0.6, 0.88
    total_x, total_y = 1.45, 0.88
    rfi_x, rfi_y = 2.3, 0.88

    # =========================
    # TQ
    # =========================
    fig.add_annotation(x=tq_x, y=tq_y+0.12, text="<b>TQ Only</b>", showarrow=False, font=dict(color="#60A5FA", size=12))
    fig.add_annotation(x=tq_x, y=tq_y, text=f"<b>{tq_pct}%</b>", showarrow=False, font=dict(color="white", size=18))
    fig.add_annotation(x=tq_x, y=tq_y-0.12, text=f"<b>{tq_total}</b>", showarrow=False, font=dict(color="white", size=22))

    # 🔥 INSIDE BOTTOM OF CIRCLE
    fig.add_annotation(
        x=tq_x, y=0.42,
        text=f"Not Responded: {tq_not}",
        showarrow=False,
        font=dict(color="#60A5FA", size=10)
    )

    # =========================
    # TOTAL
    # =========================
    fig.add_annotation(x=total_x, y=total_y+0.12, text="<b>TQ + RFI</b>", showarrow=False, font=dict(color="#A855F7", size=12))
    fig.add_annotation(x=total_x, y=total_y, text=f"<b>100%</b>", showarrow=False, font=dict(color="white", size=18))
    fig.add_annotation(x=total_x, y=total_y-0.12, text=f"<b>{total}</b>", showarrow=False, font=dict(color="white", size=22))

    fig.add_annotation(
        x=total_x, y=0.42,
        text=f"Not Responded: {total_not}",
        showarrow=False,
        font=dict(color="#A855F7", size=10)
    )

    # =========================
    # RFI
    # =========================
    fig.add_annotation(x=rfi_x, y=rfi_y+0.12, text="<b>RFI Only</b>", showarrow=False, font=dict(color="#4ADE80", size=12))
    fig.add_annotation(x=rfi_x, y=rfi_y, text=f"<b>{rfi_pct}%</b>", showarrow=False, font=dict(color="white", size=18))
    fig.add_annotation(x=rfi_x, y=rfi_y-0.12, text=f"<b>{rfi_total}</b>", showarrow=False, font=dict(color="white", size=22))

    fig.add_annotation(
        x=rfi_x, y=0.42,
        text=f"Not Responded: {rfi_not}",
        showarrow=False,
        font=dict(color="#4ADE80", size=10)
    )

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        height=250,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[0, 3.0]),
        yaxis=dict(visible=False, range=[0.2, 1.5])
    )

    st.plotly_chart(fig, use_container_width=True)
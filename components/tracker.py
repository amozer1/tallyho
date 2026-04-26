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

    # =========================
    # NOT RESPONDED
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

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

    left, right = st.columns([1, 1])

    with left:

        fig = go.Figure()

        # =========================
        # CIRCLES (UNCHANGED)
        # =========================

        fig.add_shape(
            type="circle",
            x0=0.0, y0=0.2,
            x1=1.2, y1=1.4,
            fillcolor="rgba(59,130,246,0.55)",
            line=dict(color="#3b82f6", width=2)
        )

        fig.add_shape(
            type="circle",
            x0=2.0, y0=0.2,
            x1=3.2, y1=1.4,
            fillcolor="rgba(34,197,94,0.55)",
            line=dict(color="#22c55e", width=2)
        )

        fig.add_shape(
            type="circle",
            x0=0.85, y0=0.15,
            x1=2.35, y1=1.65,
            fillcolor="rgba(168,85,247,0.80)",
            line=dict(color="#a855f7", width=3)
        )

        # =========================
        # MAIN LABELS
        # =========================

        fig.add_annotation(x=0.6, y=0.8,
                           text=f"<b>Total TQ</b><br>{tq_total}<br>{tq_pct}%",
                           showarrow=False,
                           font=dict(color="white", size=16))

        fig.add_annotation(x=1.6, y=0.82,
                           text=f"<b>Total</b><br>{total}<br>100%",
                           showarrow=False,
                           font=dict(color="white", size=18))

        fig.add_annotation(x=2.6, y=0.8,
                           text=f"<b>Total RFI</b><br>{rfi_total}<br>{rfi_pct}%",
                           showarrow=False,
                           font=dict(color="white", size=16))

        # =========================
        # 🔥 FIXED NOT RESPONDED (NO OVERLAP)
        # =========================

        fig.add_annotation(
            x=0.6, y=-0.08,
            text=f"TQ Not Responded:<br><b>{tq_not}</b> ({tq_not_pct}%)",
            showarrow=False,
            font=dict(color="#60A5FA", size=12),
            align="center"
        )

        fig.add_annotation(
            x=1.6, y=-0.08,
            text=f"Total Not Responded:<br><b>{total_not}</b> ({total_not_pct}%)",
            showarrow=False,
            font=dict(color="#F87171", size=12),
            align="center"
        )

        fig.add_annotation(
            x=2.6, y=-0.08,
            text=f"RFI Not Responded:<br><b>{rfi_not}</b> ({rfi_not_pct}%)",
            showarrow=False,
            font=dict(color="#4ADE80", size=12),
            align="center"
        )

        # =========================
        # LAYOUT FIX (IMPORTANT)
        # =========================
        fig.update_layout(
            height=380,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            margin=dict(l=0, r=0, t=0, b=0),

            xaxis=dict(visible=False, range=[-0.3, 3.6]),
            yaxis=dict(visible=False, range=[-0.5, 1.9])
        )

        st.plotly_chart(fig, use_container_width=True)
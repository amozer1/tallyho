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

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

    # =========================
    # HEADER (LIGHTER, CLEAN)
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
        # 🔵 TQ (SOFT BLUE)
        # =========================
        fig.add_shape(
            type="circle",
            x0=0.05, y0=0.30,
            x1=1.15, y1=1.40,
            fillcolor="rgba(96,165,250,0.25)",
            line=dict(color="#60A5FA", width=2)
        )

        fig.add_annotation(x=0.6, y=1.05,
                           text="<b>TQ</b>",
                           showarrow=False,
                           font=dict(color="white"))

        fig.add_annotation(x=0.6, y=0.8,
                           text=f"<b>{tq_total}</b>",
                           showarrow=False,
                           font=dict(color="#BFDBFE", size=22))

        fig.add_annotation(x=0.6, y=0.55,
                           text=f"{tq_pct}% of total",
                           showarrow=False,
                           font=dict(color="rgba(255,255,255,0.65)"))

        # =========================
        # 🟢 RFI (SOFT GREEN)
        # =========================
        fig.add_shape(
            type="circle",
            x0=2.05, y0=0.30,
            x1=3.15, y1=1.40,
            fillcolor="rgba(74,222,128,0.20)",
            line=dict(color="#4ADE80", width=2)
        )

        fig.add_annotation(x=2.6, y=1.05,
                           text="<b>RFI</b>",
                           showarrow=False,
                           font=dict(color="white"))

        fig.add_annotation(x=2.6, y=0.8,
                           text=f"<b>{rfi_total}</b>",
                           showarrow=False,
                           font=dict(color="#BBF7D0", size=22))

        fig.add_annotation(x=2.6, y=0.55,
                           text=f"{rfi_pct}% of total",
                           showarrow=False,
                           font=dict(color="rgba(255,255,255,0.65)"))

        # =========================
        # 🔴 TOTAL (LIGHT RED / ALERT STYLE)
        # =========================
        fig.add_shape(
            type="circle",
            x0=1.05, y0=0.20,
            x1=2.10, y1=1.50,
            fillcolor="rgba(248,113,113,0.18)",
            line=dict(color="#F87171", width=2)
        )

        fig.add_annotation(x=1.6, y=1.10,
                           text="<b>TOTAL</b>",
                           showarrow=False,
                           font=dict(color="white"))

        fig.add_annotation(x=1.6, y=0.80,
                           text=f"<b>{total}</b>",
                           showarrow=False,
                           font=dict(color="#FECACA", size=26))

        fig.add_annotation(x=1.6, y=0.55,
                           text="100%",
                           showarrow=False,
                           font=dict(color="rgba(255,255,255,0.65)"))

        # =========================
        # NOT RESPONDED (SIMPLIFIED TO AVOID OVERLAP)
        # =========================
        fig.add_annotation(x=0.6, y=-0.10,
                           text=f"TQ Not Responded: <b>{tq_not}</b> ({tq_not_pct}%)",
                           showarrow=False,
                           font=dict(color="#60A5FA", size=12))

        fig.add_annotation(x=1.6, y=-0.10,
                           text=f"Total Not Responded: <b>{total_not}</b> ({total_not_pct}%)",
                           showarrow=False,
                           font=dict(color="#F87171", size=12))

        fig.add_annotation(x=2.6, y=-0.10,
                           text=f"RFI Not Responded: <b>{rfi_not}</b> ({rfi_not_pct}%)",
                           showarrow=False,
                           font=dict(color="#4ADE80", size=12))

        # =========================
        # RESPONSIVE FIX
        # =========================
        fig.update_layout(
            height=380,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            margin=dict(l=10, r=10, t=10, b=20),

            # 🔥 IMPORTANT: gives breathing space to avoid overlap on small screens
            xaxis=dict(visible=False, range=[-0.3, 3.6]),
            yaxis=dict(visible=False, range=[-0.4, 1.9]),
        )

        st.plotly_chart(fig, use_container_width=True)
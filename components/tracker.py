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

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

    # =========================
    # CARD WRAPPER (THIS IS KEY)
    # =========================
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0b1220, #0f172a);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    ">
    """, unsafe_allow_html=True)

    # =========================
    # CARD HEADER
    # =========================
    st.markdown("""
    <div style="
        text-align:center;
        font-size:14px;
        font-weight:800;
        color:white;
        margin-bottom:10px;
    ">
        📊 TQ & RFI Status Overview
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # PLOTLY VISUAL (LEFT SIDE STYLE INSIDE CARD)
    # =========================
    fig = go.Figure()

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

    fig.add_annotation(x=0.6, y=0.85,
                       text=f"<b>TQ</b><br>{tq_total}",
                       showarrow=False,
                       font=dict(color="white", size=16))

    fig.add_annotation(x=1.6, y=0.9,
                       text=f"<b>TOTAL</b><br>{total}",
                       showarrow=False,
                       font=dict(color="white", size=18))

    fig.add_annotation(x=2.6, y=0.85,
                       text=f"<b>RFI</b><br>{rfi_total}",
                       showarrow=False,
                       font=dict(color="white", size=16))

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[-0.3, 3.6]),
        yaxis=dict(visible=False, range=[-0.3, 1.9]),
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # KPI STRIP (INSIDE SAME CARD)
    # =========================
    st.markdown("""
    <div style="display:flex; justify-content:space-between; gap:10px; margin-top:10px;">

        <div style="flex:1; background:#0b1220; padding:10px; border-radius:10px; text-align:center;">
            <div style="color:#60A5FA; font-size:12px;">TQ Not Responded</div>
            <div style="color:white; font-size:16px; font-weight:700;">""" + str(tq_not) + """</div>
            <div style="color:#9ca3af; font-size:11px;">""" + str(tq_not_pct) + """%</div>
        </div>

        <div style="flex:1; background:#0b1220; padding:10px; border-radius:10px; text-align:center;">
            <div style="color:#F87171; font-size:12px;">Total Not Responded</div>
            <div style="color:white; font-size:16px; font-weight:700;">""" + str(total_not) + """</div>
            <div style="color:#9ca3af; font-size:11px;">""" + str(total_not_pct) + """%</div>
        </div>

        <div style="flex:1; background:#0b1220; padding:10px; border-radius:10px; text-align:center;">
            <div style="color:#4ADE80; font-size:12px;">RFI Not Responded</div>
            <div style="color:white; font-size:16px; font-weight:700;">""" + str(rfi_not) + """</div>
            <div style="color:#9ca3af; font-size:11px;">""" + str(rfi_not_pct) + """%</div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CLOSE CARD
    # =========================
    st.markdown("</div>", unsafe_allow_html=True)
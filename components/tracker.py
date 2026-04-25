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

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([2.5, 1])

    # =========================
    # LEFT SIDE VISUAL
    # =========================
    with left:

        fig = go.Figure()

        # =========================
        # OUTER BORDER (CARD)
        # =========================
        fig.add_shape(
            type="rect",
            x0=-0.4, y0=-0.3,
            x1=3.9, y1=2.1,
            line=dict(color="rgba(255,255,255,0.25)", width=2),
            fillcolor="rgba(255,255,255,0.02)",
            layer="below"
        )

        # =========================
        # TITLE
        # =========================
        fig.add_annotation(
            x=1.7, y=1.95,
            text="<b>TQ AND RFI OVERVIEW</b>",
            showarrow=False,
            font=dict(size=22, color="white")
        )

        # =========================
        # CIRCLES (SAME SIZE)
        # =========================

        radius = 1.1

        # LEFT - TQ (blue)
        fig.add_shape(
            type="circle",
            x0=0.2, y0=0.25,
            x1=0.2 + radius, y1=0.25 + radius,
            fillcolor="rgba(59,130,246,0.45)",
            line=dict(color="#3b82f6", width=4),
            layer="below"
        )

        # RIGHT - RFI (green)
        fig.add_shape(
            type="circle",
            x0=2.0, y0=0.25,
            x1=2.0 + radius, y1=0.25 + radius,
            fillcolor="rgba(34,197,94,0.45)",
            line=dict(color="#22c55e", width=4),
            layer="below"
        )

        # =========================
        # MIDDLE - TOTAL (LIGHT RED, DOMINANT)
        # =========================
        fig.add_shape(
            type="circle",
            x0=1.1, y0=0.15,
            x1=1.1 + radius + 0.2,
            y1=0.15 + radius + 0.2,
            fillcolor="rgba(255,99,99,0.65)",  # light red
            line=dict(color="#ff4d4d", width=5),
            layer="above"
        )

        # =========================
        # TEXT (READABLE CARDS)
        # =========================

        def label(x, y, title, value, pct):
            fig.add_annotation(
                x=x, y=y,
                showarrow=False,
                text=f"""
                <div style="
                    background: rgba(0,0,0,0.55);
                    padding: 10px 14px;
                    border-radius: 10px;
                    text-align:center;
                    color:white;
                    font-family:Arial;
                ">
                    <b>{title}</b><br>
                    <span style="font-size:24px">{value}</span><br>
                    <span style="font-size:12px">{pct}%</span>
                </div>
                """
            )

        label(0.65, 0.75, "TQ", tq_total, tq_pct)
        label(1.75, 0.85, "TOTAL", total, 100)
        label(2.75, 0.75, "RFI", rfi_total, rfi_pct)

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(
            height=400,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.5, 4.2]),
            yaxis=dict(visible=False, range=[-0.4, 2.3]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("#### ⚙ Control Panel")

        st.markdown(f"""
🔵 **TQ not responded**  
**{tq_not} ({round((tq_not/tq_total)*100,1) if tq_total else 0}%)**

🟢 **RFI not responded**  
**{rfi_not} ({round((rfi_not/rfi_total)*100,1) if rfi_total else 0}%)**

⚫ **Total not responded**  
**{total_not} ({round((total_not/total)*100,1) if total else 0}%)**
""")

        st.markdown("---")

        st.error(
            f"⚠ Outstanding > 7 Days: {overdue} ({round((overdue/total)*100,1) if total else 0}%)"
        )
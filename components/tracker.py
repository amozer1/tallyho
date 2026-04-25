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

    # =========================
    # OUTSTANDING > 7 DAYS
    # =========================
    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([2.5, 1])

    # =========================
    # LEFT SIDE (CIRCLES + BORDER CARD)
    # =========================
    with left:

        fig = go.Figure()

        # =========================
        # OUTER BORDER RECTANGLE (CARD)
        # =========================
        fig.add_shape(
            type="rect",
            x0=-0.3, y0=-0.2,
            x1=3.5, y1=2.0,
            line=dict(color="rgba(255,255,255,0.35)", width=2),
            fillcolor="rgba(255,255,255,0.03)",
            layer="below"
        )

        # =========================
        # TITLE ABOVE CIRCLES
        # =========================
        fig.add_annotation(
            x=1.6, y=1.85,
            text="<b>TQ AND RFI OVERVIEW</b>",
            showarrow=False,
            font=dict(size=20, color="white"),
            align="center"
        )

        # =========================
        # CIRCLES
        # =========================

        # TQ
        fig.add_shape(
            type="circle",
            x0=0.1, y0=0.2,
            x1=1.3, y1=1.4,
            fillcolor="rgba(59,130,246,0.45)",
            line=dict(color="#3b82f6", width=4),
            layer="below"
        )

        # RFI
        fig.add_shape(
            type="circle",
            x0=1.9, y0=0.2,
            x1=3.1, y1=1.4,
            fillcolor="rgba(34,197,94,0.45)",
            line=dict(color="#22c55e", width=4),
            layer="below"
        )

        # TOTAL (middle, slightly larger)
        fig.add_shape(
            type="circle",
            x0=0.95, y0=0.05,
            x1=2.35, y1=1.55,
            fillcolor="rgba(168,85,247,0.65)",
            line=dict(color="#a855f7", width=5),
            layer="above"
        )

        # =========================
        # TEXT INSIDE CIRCLES
        # =========================

        fig.add_annotation(
            x=0.7, y=0.8,
            text=f"<b>Total TQ</b><br><span style='font-size:26px'>{tq_total}</span><br>{tq_pct}%",
            showarrow=False,
            font=dict(color="white")
        )

        fig.add_annotation(
            x=1.65, y=0.85,
            text=f"<b>Total</b><br><span style='font-size:32px'>{total}</span><br>100%",
            showarrow=False,
            font=dict(color="white")
        )

        fig.add_annotation(
            x=2.6, y=0.8,
            text=f"<b>Total RFI</b><br><span style='font-size:26px'>{rfi_total}</span><br>{rfi_pct}%",
            showarrow=False,
            font=dict(color="white")
        )

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(
            height=360,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.5, 3.7]),
            yaxis=dict(visible=False, range=[-0.3, 2.1]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RIGHT SIDE CONTROL PANEL
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
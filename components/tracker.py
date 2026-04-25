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
        # BACKGROUND CARD BORDER
        # =========================
        fig.add_shape(
            type="rect",
            x0=-0.4, y0=-0.3,
            x1=3.8, y1=2.2,
            line=dict(color="rgba(255,120,120,0.35)", width=2),
            fillcolor="rgba(255,80,80,0.05)",
            layer="below"
        )

        # =========================
        # TITLE
        # =========================
        fig.add_annotation(
            x=1.7, y=2.05,
            text="<b>TQ AND RFI OVERVIEW</b>",
            showarrow=False,
            font=dict(size=22, color="white")
        )

        # =========================
        # CIRCLES (OVERLAPPING ALLOWED)
        # LIGHT RED THEME
        # =========================

        # TQ (left)
        fig.add_shape(
            type="circle",
            x0=0.2, y0=0.3,
            x1=1.35, y1=1.45,
            fillcolor="rgba(255,99,132,0.45)",
            line=dict(color="rgba(255,120,120,1)", width=3),
            layer="below"
        )

        # RFI (right)
        fig.add_shape(
            type="circle",
            x0=2.2, y0=0.3,
            x1=3.35, y1=1.45,
            fillcolor="rgba(255,160,122,0.45)",
            line=dict(color="rgba(255,140,100,1)", width=3),
            layer="below"
        )

        # =========================
        # MIDDLE (TOTAL - DOMINANT)
        # BIGGER + HIGHER OPACITY + ABOVE
        # =========================
        fig.add_shape(
            type="circle",
            x0=1.05, y0=0.05,
            x1=2.85, y1=1.75,
            fillcolor="rgba(220,20,60,0.75)",
            line=dict(color="rgba(255,80,80,1)", width=5),
            layer="above"
        )

        # =========================
        # TEXT FUNCTION (READABLE BADGES)
        # =========================
        def badge(x, y, title, value, pct):
            fig.add_annotation(
                x=x,
                y=y,
                showarrow=False,
                text=f"""
                <div style="
                    background: rgba(0,0,0,0.55);
                    padding: 10px 12px;
                    border-radius: 12px;
                    color: white;
                    text-align:center;
                    min-width:90px;
                ">
                    <b>{title}</b><br>
                    <span style="font-size:22px">{value}</span><br>
                    <span style="font-size:12px">{pct}%</span>
                </div>
                """
            )

        # LEFT
        badge(0.75, 0.85, "TQ", tq_total, tq_pct)

        # MIDDLE (dominant)
        badge(1.95, 0.95, "TOTAL", total, 100)

        # RIGHT
        badge(2.95, 0.85, "RFI", rfi_total, rfi_pct)

        # =========================
        # LAYOUT SETTINGS
        # =========================
        fig.update_layout(
            height=400,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.5, 4.0]),
            yaxis=dict(visible=False, range=[-0.4, 2.4]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("#### ⚙ Control Panel")

        st.markdown(f"""
🔴 **TQ not responded**  
**{tq_not} ({round((tq_not/tq_total)*100,1) if tq_total else 0}%)**

🟠 **RFI not responded**  
**{rfi_not} ({round((rfi_not/rfi_total)*100,1) if rfi_total else 0}%)**

⚫ **Total not responded**  
**{total_not} ({round((total_not/total)*100,1) if total else 0}%)**
""")

        st.markdown("---")

        st.error(
            f"⚠ Outstanding > 7 Days: {overdue} ({round((overdue/total)*100,1) if total else 0}%)"
        )
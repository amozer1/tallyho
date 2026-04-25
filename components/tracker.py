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

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([3, 1])

    # =========================
    # LEFT VISUAL
    # =========================
    with left:

        fig = go.Figure()

        # MAIN CONTAINER
        fig.add_shape(
            type="rect",
            x0=0, y0=0,
            x1=10, y1=6,
            line=dict(color="rgba(255,255,255,0.5)", width=2),
            fillcolor="rgba(0,0,0,0)",
        )

        # RIGHT SIDE KPI PANEL (CLEAN & SIMPLE)
        fig.add_shape(
            type="rect",
            x0=7.2, y0=0.5,
            x1=9.7, y1=5.5,
            line=dict(color="rgba(255,255,255,0.3)", width=1.5),
            fillcolor="rgba(255,255,255,0.03)",
        )

        # HEADER ONLY (NO CLUTTER)
        fig.add_annotation(
            x=4.5, y=5.6,
            text="<b>Not Responded Within 7 Days</b><br><span style='font-size:12px'>TQ & RFI AGING OVERVIEW</span>",
            showarrow=False,
            font=dict(color="white", size=18),
        )

        # =========================
        # SIMPLE CLEAN CIRCLES (NO OVERLAP TEXT INSIDE ANNOTATIONS)
        # =========================
        fig.add_shape(
            type="circle",
            x0=1, y0=1, x1=4, y1=4,
            fillcolor="rgba(59,130,246,0.55)",
            line=dict(color="#3b82f6", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=3.5, y0=1, x1=6.5, y1=4,
            fillcolor="rgba(168,85,247,0.6)",
            line=dict(color="#a855f7", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=2.5, y0=0.8, x1=5.5, y1=4.8,
            fillcolor="rgba(34,197,94,0.4)",
            line=dict(color="#22c55e", width=2),
        )

        # SIMPLE LABELS (ONLY 3 — CLEAN)
        fig.add_annotation(x=2.5, y=2.5,
            text=f"<b>TQ</b><br>{tq_total}",
            showarrow=False, font=dict(color="white"))

        fig.add_annotation(x=4.5, y=2.5,
            text=f"<b>TOTAL</b><br>{total}",
            showarrow=False, font=dict(color="white"))

        fig.add_annotation(x=6.0, y=2.5,
            text=f"<b>RFI</b><br>{rfi_total}",
            showarrow=False, font=dict(color="white"))

        # =========================
        # RIGHT PANEL TEXT (ONLY PLACE FOR KPI TEXT)
        # =========================
        fig.add_annotation(
            x=8.4, y=5.0,
            text=f"""
⚙ <b>Summary</b><br><br>

🔵 TQ Not Responded:<br>
<b>{tq_not} ({tq_not_pct}%)</b><br><br>

🟢 RFI Not Responded:<br>
<b>{rfi_not} ({rfi_not_pct}%)</b><br><br>

⚫ Total Not Responded:<br>
<b>{total_not} ({total_not_pct}%)</b><br><br>

⚠ Overdue > 7 Days:<br>
<b>{overdue}</b>
""",
            showarrow=False,
            align="left",
            font=dict(color="white", size=12)
        )

        # =========================
        # FINAL LAYOUT
        # =========================
        fig.update_layout(
            height=450,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[0, 10]),
            yaxis=dict(visible=False, range=[0, 6]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # STREAMLIT SIDE SUMMARY
    # =========================
    with right:
        st.markdown("#### ⚙ Summary")

        st.markdown(f"""
🔵 TQ Not Responded: **{tq_not} ({tq_not_pct}%)**

🟢 RFI Not Responded: **{rfi_not} ({rfi_not_pct}%)**

⚫ Total Not Responded: **{total_not} ({total_not_pct}%)**
""")

        st.error(f"⚠ Overdue > 7 Days: {overdue}")
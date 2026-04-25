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

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([3, 1])

    # =========================
    # LEFT CHART
    # =========================
    with left:

        fig = go.Figure()

        # =========================
        # MAIN BOUNDARY
        # =========================
        fig.add_shape(
            type="rect",
            x0=-0.6, y0=-0.2,
            x1=3.6, y1=1.9,
            line=dict(color="rgba(255,255,255,0.6)", width=2),
            fillcolor="rgba(0,0,0,0)",
        )

        # =========================
        # RIGHT KPI PANEL (CLEAN BOX)
        # =========================
        fig.add_shape(
            type="rect",
            x0=2.55, y0=0.1,
            x1=3.5, y1=1.7,
            line=dict(color="rgba(255,255,255,0.4)", width=1.5),
            fillcolor="rgba(255,255,255,0.03)",
        )

        # =========================
        # CIRCLES (SLIGHTLY REDUCED SIZE FOR FIT)
        # =========================
        fig.add_shape(
            type="circle",
            x0=0.1, y0=0.35, x1=1.1, y1=1.35,
            fillcolor="rgba(59,130,246,0.55)",
            line=dict(color="#3b82f6", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=1.4, y0=0.35, x1=2.4, y1=1.35,
            fillcolor="rgba(168,85,247,0.65)",
            line=dict(color="#a855f7", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=0.75, y0=0.15, x1=1.85, y1=1.55,
            fillcolor="rgba(34,197,94,0.45)",
            line=dict(color="#22c55e", width=2),
        )

        # =========================
        # LABELS
        # =========================
        fig.add_annotation(
            x=0.6, y=0.85,
            text=f"<b>TQ</b><br>{tq_total}<br>{tq_pct}%",
            showarrow=False,
            font=dict(color="white", size=14)
        )

        fig.add_annotation(
            x=1.65, y=0.9,
            text=f"<b>TOTAL</b><br>{total}<br>100%",
            showarrow=False,
            font=dict(color="white", size=16)
        )

        fig.add_annotation(
            x=2.2, y=0.85,
            text=f"<b>RFI</b><br>{rfi_total}<br>{rfi_pct}%",
            showarrow=False,
            font=dict(color="white", size=14)
        )

        # =========================
        # RIGHT KPI PANEL TEXT (CLEAN BULLETS)
        # =========================
        fig.add_annotation(
            x=3.05, y=1.55,
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
            font=dict(color="white", size=12),
            align="left"
        )

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(
            height=420,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.6, 3.6]),
            yaxis=dict(visible=False, range=[-0.2, 1.9]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # STREAMLIT SIDE PANEL
    # =========================
    with right:
        st.markdown("#### ⚙ Summary")

        st.markdown(f"""
🔵 **TQ Not Responded:** {tq_not} ({tq_not_pct}%)

🟢 **RFI Not Responded:** {rfi_not} ({rfi_not_pct}%)

⚫ **Total Not Responded:** {total_not} ({total_not_pct}%)
""")

        st.error(f"⚠ Overdue > 7 Days: {overdue}")
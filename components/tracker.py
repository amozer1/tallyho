import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    # -------------------------
    # CLEAN DATA
    # -------------------------
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

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

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # -------------------------
    # TITLE
    # -------------------------
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([2.4, 1])

    # -------------------------
    # KPI CIRCLES
    # -------------------------
    with left:
        fig = go.Figure()

        # Circle positions tighter together
        circles = [
            (-0.1, 0.1, 1.2, 1.4, "rgba(59,130,246,0.55)", "#3b82f6"),
            (0.9, 0.1, 2.2, 1.4, "rgba(168,85,247,0.55)", "#a855f7"),
            (1.9, 0.1, 3.2, 1.4, "rgba(34,197,94,0.55)", "#22c55e"),
        ]

        for x0, y0, x1, y1, fill, line in circles:
            fig.add_shape(
                type="circle",
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,
                fillcolor=fill,
                line=dict(color=line, width=4),
            )

        # annotations
        fig.add_annotation(
            x=0.55, y=0.75,
            text=f"<b>Total TQ</b><br><span style='font-size:28px'>{tq_total}</span><br>{tq_pct}%",
            showarrow=False,
            font=dict(color="white", size=16),
            align="center"
        )

        fig.add_annotation(
            x=1.55, y=0.75,
            text=f"<b>Total RFI</b><br><span style='font-size:28px'>{rfi_total}</span><br>{rfi_pct}%",
            showarrow=False,
            font=dict(color="white", size=16),
            align="center"
        )

        fig.add_annotation(
            x=2.55, y=0.75,
            text=f"<b>Total</b><br><span style='font-size:28px'>{total}</span><br>100%",
            showarrow=False,
            font=dict(color="white", size=16),
            align="center"
        )

        fig.update_layout(
            height=300,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.3, 3.3]),
            yaxis=dict(visible=False, range=[0, 1.5]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # CONTROL PANEL
    # -------------------------
    with right:
        st.markdown("#### ⚙ Control Panel")

        st.markdown(f"""
🔵 **TQ not responded**  
**{tq_not} ({round((tq_not/tq_total)*100,1) if tq_total else 0}%)**

🟣 **RFI not responded**  
**{rfi_not} ({round((rfi_not/rfi_total)*100,1) if rfi_total else 0}%)**

⚫ **Total not responded**  
**{total_not} ({round((total_not/total)*100,1) if total else 0}%)**
""")

        st.markdown("---")

        st.error(
            f"⚠ Outstanding > 7 Days: {overdue} ({round((overdue/total)*100,1) if total else 0}%)"
        )
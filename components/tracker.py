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
    # OVERDUE (>7 DAYS)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_tq = len(overdue_df[overdue_df["doc type"].str.lower() == "tq"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"].str.lower() == "rfi"])

    overdue_total_pct = round((overdue_total / total) * 100, 1) if total else 0

    # =========================
    # CLEAN STATIC ALERT (NO FLASHING)
    # =========================
    st.markdown(
        f"""
        <div style="
            padding: 10px;
            border: 1px solid rgba(255, 80, 80, 0.5);
            background-color: rgba(255, 80, 80, 0.08);
            border-radius: 6px;
            margin-bottom: 10px;
            color: #ff4d4d;
            font-weight: 600;
        ">
            ⚠ Outstanding > 7 Days: {overdue_total} ({overdue_total_pct}%)
            <br>
            🔵 TQ: {overdue_tq} | 🟢 RFI: {overdue_rfi}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Tracker")

    left, right = st.columns([2.5, 1])

    # =========================
    # LEFT VISUAL
    # =========================
    with left:

        fig = go.Figure()

        # =========================
        # BOUNDARY (TIGHT AROUND CONTENT)
        # =========================
        fig.add_shape(
            type="rect",
            x0=-0.1, y0=-0.2,
            x1=3.3, y1=1.8,
            line=dict(color="rgba(255,255,255,0.6)", width=2),
            fillcolor="rgba(0,0,0,0)"
        )

        # =========================
        # HEADER
        # =========================
        fig.add_annotation(
            x=1.6, y=1.65,
            text="<b>Not Responded Within 7 Days</b><br><span style='font-size:12px'>TQ & RFI AGING OVERVIEW</span>",
            showarrow=False,
            font=dict(color="white", size=16),
        )

        # =========================
        # CIRCLES (UNCHANGED LOGIC)
        # =========================
        fig.add_shape(
            type="circle",
            x0=0.1, y0=0.2, x1=1.2, y1=1.4,
            fillcolor="rgba(59,130,246,0.55)",
            line=dict(color="#3b82f6", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=1.9, y0=0.2, x1=3.0, y1=1.4,
            fillcolor="rgba(34,197,94,0.55)",
            line=dict(color="#22c55e", width=2),
        )

        fig.add_shape(
            type="circle",
            x0=0.9, y0=0.05, x1=2.2, y1=1.55,
            fillcolor="rgba(168,85,247,0.70)",
            line=dict(color="#a855f7", width=2),
        )

        # =========================
        # LABELS
        # =========================
        fig.add_annotation(x=0.6, y=0.8,
            text=f"<b>TQ</b><br>{tq_total}<br>{tq_pct}%",
            showarrow=False, font=dict(color="white"))

        fig.add_annotation(x=1.55, y=0.85,
            text=f"<b>TOTAL</b><br>{total}<br>100%",
            showarrow=False, font=dict(color="white"))

        fig.add_annotation(x=2.5, y=0.8,
            text=f"<b>RFI</b><br>{rfi_total}<br>{rfi_pct}%",
            showarrow=False, font=dict(color="white"))

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(
            height=380,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False, range=[-0.2, 3.2]),
            yaxis=dict(visible=False, range=[-0.2, 1.8]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("#### ⚙ Control Panel")

        st.markdown(f"""
🔵 TQ Not Responded: **{tq_not} ({tq_not_pct}%)**

🟢 RFI Not Responded: **{rfi_not} ({rfi_not_pct}%)**

⚫ Total Not Responded: **{total_not} ({total_not_pct}%)**
""")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    # =========================
    # SAFETY
    # =========================
    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = ["doc type", "date sent", "reply date", "status"]

    if not all(col in df.columns for col in required_cols):
        st.error("Missing required columns.")
        return

    # =========================
    # DATA
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
    combined_total = tq_total + rfi_total

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    overdue_count = len(df[df["age"] > 7])

    # =========================
    # TITLE
    # =========================
    st.markdown("## 📊 TQ & RFI Tracker Overview")

    left, right = st.columns([1.7, 1])

    # =========================
    # KPI CIRCLE (TRUE CENTERED CARD)
    # =========================
    def kpi_circle(value, base, color, label, key):

        base = base if base > 0 else 1
        pct = round((value / base) * 100, 1)

        fig = go.Figure(go.Pie(
            values=[value, base - value],
            hole=0.80,
            marker=dict(colors=[color, "#e5e7eb"]),
            textinfo="none"
        ))

        fig.update_layout(
            height=270,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)"
        )

        # =========================
        # CLEAN BACKGROUND CARD INSIDE DONUT
        # =========================
        fig.add_shape(
            type="circle",
            x0=0.32, x1=0.68,
            y0=0.32, y1=0.68,
            fillcolor="white",
            line=dict(color="rgba(0,0,0,0)"),
            layer="above"
        )

        # =========================
        # CENTER KPI TEXT (PROPERLY ALIGNED)
        # =========================
        fig.add_annotation(
            x=0.5,
            y=0.52,
            text=f"""
            <b style='font-size:26px;color:#111827'>{value}</b><br>
            <span style='font-size:13px;color:#374151'>{label}</span><br>
            <span style='font-size:12px;color:#6b7280'>{pct}%</span>
            """,
            showarrow=False,
            align="center"
        )

        st.plotly_chart(fig, use_container_width=True, key=key)

    # =========================
    # LEFT: KPI CIRCLES
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_circle(tq_total, total, "#3b82f6", "Total TQ", "kpi_tq")

        with c2:
            kpi_circle(rfi_total, total, "#f59e0b", "Total RFI", "kpi_rfi")

        with c3:
            kpi_circle(combined_total, total, "#22c55e", "TQ + RFI", "kpi_total")

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("### ⚙ Control Panel")

        st.markdown(f"""
        <div style="
            background:#0f172a;
            color:#f8fafc;
            padding:18px;
            border-radius:14px;
            line-height:2;
        ">
        🔵 <b>TQ not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br>

        🟠 <b>RFI not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br>

        ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # FOOTER
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:#fee2e2;
        border-left:6px solid #ef4444;
        padding:14px;
        border-radius:10px;
        font-weight:600;
    ">
    ⚠ Outstanding > 7 Days: {overdue_count} ({round(overdue_count/total*100,1) if total else 0}%)
    </div>
    """, unsafe_allow_html=True)
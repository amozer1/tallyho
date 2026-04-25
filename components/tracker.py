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
    # LAYOUT
    # =========================
    left, right = st.columns([1.7, 1])

    # =========================
    # 🟦 KPI CIRCLE (INSIDE TEXT FIXED)
    # =========================
    def kpi_circle(value, base, color, label):
        base = base if base > 0 else 1
        pct = round((value / base) * 100, 1)

        fig = go.Figure(go.Pie(
            values=[value, base - value],
            hole=0.75,
            marker=dict(colors=[color, "#eef2f7"]),
            textinfo="none"
        ))

        fig.update_layout(
            height=260,
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )

        # 🔥 CENTER TEXT (THIS IS THE KEY FIX)
        fig.add_annotation(
            text=f"""
            <b style='font-size:20px'>{value}</b><br>
            <span style='font-size:12px;color:gray'>{label}</span><br>
            <span style='font-size:11px;color:#9ca3af'>{pct}%</span>
            """,
            x=0.5, y=0.5,
            font=dict(size=14),
            showarrow=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # LEFT SIDE
    # =========================
    with left:
        st.markdown("### 📊 TQ & RFI Tracker Overview")

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_circle(tq_total, total, "#3b82f6", "TQ")

        with c2:
            kpi_circle(rfi_total, total, "#f59e0b", "RFI")

        with c3:
            kpi_circle(combined_total, total, "#22c55e", "TOTAL")

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
        🔵 TQ not responded: <b>{tq_not}</b><br>
        🟠 RFI not responded: <b>{rfi_not}</b><br>
        ⚫ Total not responded: <b>{total_not}</b>
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
    ⚠ Outstanding > 7 Days: {overdue_count}
    </div>
    """, unsafe_allow_html=True)
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

    overdue = len(df[df["age"] > 7])

    # =========================
    # TITLE
    # =========================
    st.markdown("## 📊 TQ & RFI Tracker Overview")

    # =========================
    # LAYOUT FIX (CRITICAL)
    # =========================
    left, right = st.columns([2, 1])

    # =========================
    # KPI FUNCTION (CLEAN)
    # =========================
    def kpi(value, base, color, label, key):

        base = base if base > 0 else 1
        pct = round((value / base) * 100, 1)

        fig = go.Figure(go.Pie(
            values=[value, base - value],
            hole=0.75,
            marker=dict(colors=[color, "#eef2f7"]),
            textinfo="none"
        ))

        fig.update_layout(
            height=250,
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True, key=key)

        # ONLY PURE CENTER TEXT (NO FLOATING HTML)
        st.markdown(
            f"""
            <div style="text-align:center;margin-top:-130px;">
                <div style="font-size:24px;font-weight:700;">
                    {value}
                </div>
                <div style="font-size:13px;color:gray;">
                    {label}
                </div>
                <div style="font-size:12px;color:#9ca3af;">
                    {pct}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # LEFT KPIS
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi(tq_total, total, "#3b82f6", "TQ", "kpi1")

        with c2:
            kpi(rfi_total, total, "#f59e0b", "RFI", "kpi2")

        with c3:
            kpi(combined_total, total, "#22c55e", "TOTAL", "kpi3")

    # =========================
    # RIGHT CONTROL PANEL (FIXED CARD)
    # =========================
    with right:

        st.markdown(
            f"""
            <div style="
                background:#0f172a;
                color:#f8fafc;
                padding:18px;
                border-radius:14px;
                height:260px;
            ">

            <h4 style="margin-bottom:10px;">⚙ Control Panel</h4>

            🔵 <b>TQ not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br><br>

            🟠 <b>RFI not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br><br>

            ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)

            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # FOOTER RISK STRIP
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            background:#fee2e2;
            border-left:6px solid #ef4444;
            padding:14px;
            border-radius:10px;
            font-weight:600;
        ">
        ⚠ Outstanding > 7 Days: {overdue}
        </div>
        """,
        unsafe_allow_html=True
    )
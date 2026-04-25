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

    overdue = len(df[df["age"] > 7])

    left, right = st.columns([1.7, 1])

    # =========================
    # 🎯 PRO KPI CIRCLE
    # =========================
    def kpi_circle(value, base, color, label):
        base = base if base > 0 else 1
        pct = round((value / base) * 100, 1)

        col1, col2 = st.columns([1, 1])

        with col1:
            fig = go.Figure(go.Pie(
                values=[value, base - value],
                hole=0.78,
                marker=dict(colors=[color, "#eef2f7"]),
                textinfo="none"
            ))

            fig.update_layout(
                height=260,
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

            # 🚨 DO NOT print HTML under chart anymore

        with col2:
            # ✅ PROPER KPI CARD (NOT FLOATING HTML)
            st.markdown(f"""
            <div style="
                height:260px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                background:#f9fafb;
                border-radius:12px;
                border:1px solid #e5e7eb;
            ">

                <div style="font-size:34px;font-weight:700;color:#111827;">
                    {value}
                </div>

                <div style="font-size:14px;color:#6b7280;margin-top:6px;">
                    {label}
                </div>

                <div style="font-size:13px;color:#9ca3af;margin-top:4px;">
                    {pct}%
                </div>

            </div>
            """, unsafe_allow_html=True)

        # 🔵 chart only (clean ring)
        st.plotly_chart(fig, use_container_width=True)

        # 🟢 PERFECT CENTER OVERLAY (REAL FIX)
        st.markdown(
            f"""
            <div style="
                position: relative;
                top: -170px;
                text-align: center;
                pointer-events: none;
            ">
                <div style="
                    font-size:26px;
                    font-weight:700;
                    color:#111827;
                ">
                    {value}
                </div>

                <div style="
                    font-size:13px;
                    color:#6b7280;
                    margin-top:-4px;
                ">
                    {label}
                </div>

                <div style="
                    font-size:12px;
                    color:#9ca3af;
                    margin-top:2px;
                ">
                    {pct}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # LEFT
    # =========================
    with left:
        st.markdown("### 📊 TQ & RFI Tracker")

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

        st.markdown("""
        <div style="
            background:#0f172a;
            color:#f8fafc;
            padding:18px;
            border-radius:14px;
            line-height:2;
        ">
        KPI Status Summary
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        background:#fee2e2;
        border-left:6px solid #ef4444;
        padding:14px;
        border-radius:10px;
        font-weight:600;
    ">
    ⚠ Outstanding > 7 Days: {overdue}
    </div>
    """, unsafe_allow_html=True)
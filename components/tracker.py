import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    # =========================
    # SAFETY CHECKS
    # =========================
    if df is None or df.empty:
        st.warning("No data available in tracker.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = ["doc type", "date sent", "reply date", "status"]

    if not all(col in df.columns for col in required_cols):
        st.error(f"Missing required columns: {required_cols}")
        return

    # =========================
    # DATE PROCESSING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    # =========================
    # FILTERS (LINKED TO YOUR DATA)
    # =========================
    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)
    combined_total = tq_total + rfi_total

    # =========================
    # NOT RESPONDED LOGIC
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    # =========================
    # OUTSTANDING (>7 DAYS)
    # =========================
    overdue = df[df["age"] > 7]
    overdue_count = len(overdue)

    # =========================================================
    # 🟦 LEFT: KPI CIRCLES
    # =========================================================
    left, right = st.columns([1.6, 1])

    with left:

        c1, c2, c3 = st.columns(3)

        def draw_kpi(value, base, color, label):
            base = base if base > 0 else 1

            fig = go.Figure(go.Pie(
                values=[value, base - value],
                hole=0.72,
                marker=dict(colors=[color, "#f3f4f6"]),
                textinfo="none"
            ))

            fig.update_layout(
                height=240,
                showlegend=False,
                margin=dict(t=10, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f"""
                <div style="text-align:center">
                    <b>{label}</b><br>
                    <h3>{value}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c1:
            draw_kpi(tq_total, total, "#4da3ff", "TQ Volume")

        with c2:
            draw_kpi(rfi_total, total, "#fbbf24", "RFI Volume")

        with c3:
            draw_kpi(combined_total, total, "#22c55e", "Total Workload")

    # =========================================================
    # 🟪 RIGHT: CONTROL PANEL
    # =========================================================
    with right:

        st.markdown(f"""
        <div style="
            padding:16px;
            border-radius:12px;
            border:1px solid #e5e5e5;
            background:#fafafa;
        ">
        <h4>TQ & RFI Tracker</h4>

        🔵 <b>TQ not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br><br>

        🟠 <b>RFI not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br><br>

        ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)

        </div>
        """, unsafe_allow_html=True)

    # =========================================================
    # 🟥 FOOTER: RISK STRIP
    # =========================================================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        padding:14px;
        border-radius:10px;
        border-left:6px solid #ef4444;
        background:#fff5f5;
    ">
    ⚠ <b>Outstanding > 7 Days:</b> {overdue_count} ({round(overdue_count/total*100,1) if total else 0}%)
    </div>
    """, unsafe_allow_html=True)
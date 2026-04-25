import streamlit as st
import pandas as pd
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

    left, right = st.columns([2, 1])

    # =========================
    # PURE KPI CARD (NO RING)
    # =========================
    def kpi_card(value, label, subtext, color):

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:28px 10px;
                border-radius:18px;
                text-align:center;
                color:white;
                box-shadow:0 6px 18px rgba(0,0,0,0.1);
                height:160px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
            ">

                <div style="font-size:34px;font-weight:700;">
                    {value}
                </div>

                <div style="font-size:15px;font-weight:500;margin-top:6px;">
                    {label}
                </div>

                <div style="font-size:13px;opacity:0.9;margin-top:4px;">
                    {subtext}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # LEFT KPI SECTION
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card(tq_total, "TOTAL TQ", f"{round(tq_total/total*100,1) if total else 0}%", "#3b82f6")

        with c2:
            kpi_card(rfi_total, "TOTAL RFI", f"{round(rfi_total/total*100,1) if total else 0}%", "#f59e0b")

        with c3:
            kpi_card(combined_total, "TQ + RFI", "100%", "#22c55e")

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
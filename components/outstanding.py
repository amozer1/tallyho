import streamlit as st
import pandas as pd


def render_outstanding_line(df, total):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or len(df) == 0 or total == 0:
        st.warning("No data available")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    # =========================
    # OVERDUE FILTER (>7 DAYS + NOT REPLIED)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue = len(overdue_df)
    overdue_pct = round((overdue / total) * 100, 1) if total else 0

    # =========================
    # BREAKDOWN
    # =========================
    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    # =========================
    # ALERT CARD UI
    # =========================
    st.markdown(f"""
    <div style="
        background: #2b0b0b;
        border-left: 6px solid #ff0000;
        padding: 16px 18px;
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(255,0,0,0.25);
    ">

        <div style="
            font-size: 18px;
            font-weight: 700;
            color: #ff4d4d;
            margin-bottom: 8px;
        ">
            🚨 CRITICAL: Overdue Items (>7 days)
        </div>

        <div style="
            font-size: 16px;
            color: #ffffff;
            margin-bottom: 12px;
        ">
            <b>{overdue}</b> ({overdue_pct}%) total overdue
        </div>

        <div style="
            display: flex;
            gap: 10px;
        ">

            <div style="
                background: #1a1a1a;
                padding: 6px 12px;
                border-radius: 6px;
                color: #4da3ff;
                font-weight: 600;
            ">
                TQ: {overdue_tq}
            </div>

            <div style="
                background: #1a1a1a;
                padding: 6px 12px;
                border-radius: 6px;
                color: #00c853;
                font-weight: 600;
            ">
                RFI: {overdue_rfi}
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)
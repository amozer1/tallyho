import streamlit as st
import pandas as pd


def render_outstanding_line(df, total):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or len(df) == 0 or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    # =========================
    # OVERDUE LOGIC
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue = len(overdue_df)
    overdue_pct = round((overdue / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    # =========================
    # UI
    # =========================
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #2b0b0b, #140404);
        border-left: 8px solid red;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(255,0,0,0.25);
        margin-bottom: 15px;
    ">

        <div style="
            font-size: 26px;
            font-weight: 800;
            color: white;
            line-height: 1;
        ">
            🚨 {overdue}
        </div>

        <div style="
            font-size: 14px;
            color: #d1d5db;
            margin-top: 4px;
            margin-bottom: 12px;
        ">
            {overdue_pct}% overdue
        </div>

        <div style="
            display:flex;
            gap:10px;
        ">

            <div style="
                background:#111827;
                color:#4da3ff;
                padding:6px 12px;
                border-radius:20px;
                font-weight:700;
                font-size:13px;
            ">
                TQ {overdue_tq}
            </div>

            <div style="
                background:#111827;
                color:#00c853;
                padding:6px 12px;
                border-radius:20px;
                font-weight:700;
                font-size:13px;
            ">
                RFI {overdue_rfi}
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)
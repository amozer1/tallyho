import streamlit as st
import pandas as pd


def render_outstanding_line(df, total):
    """
    Displays overdue summary line using actual dataframe.
    """

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or df.empty or total == 0:
        st.warning("No outstanding data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    if "doc type" not in df.columns or "reply date" not in df.columns or "age" not in df.columns:
        st.error("Required columns missing: 'doc type', 'reply date', or 'age'")
        return

    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    # =========================
    # TOTALS
    # =========================
    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    # =========================
    # OVERDUE LOGIC
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1) if total else 0

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # UI
    # =========================
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #111827, #1f2937);
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        color: white;
        font-family: Arial;
        margin-bottom: 15px;
    ">

        <div style="
            font-size:24px;
            font-weight:700;
            color:#ef4444;
        ">
            🚨 Overdue (&gt; 7 days) = {overdue_total} ({overdue_pct}%)
        </div>

        <div style="
            margin-top:10px;
            font-size:18px;
            color:#fbbf24;
        ">
            📌 TQ overdue = {overdue_tq} ({tq_pct}% of TQ total)
        </div>

        <div style="
            margin-top:6px;
            font-size:18px;
            color:#38bdf8;
        ">
            📌 RFI overdue = {overdue_rfi} ({rfi_pct}% of RFI total)
        </div>

    </div>
    """, unsafe_allow_html=True)
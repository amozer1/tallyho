import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    # =========================
    # OVERDUE (>7 DAYS)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # CARD (MATCH age_outstanding STYLE)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:10px;
        height:200px;
    ">
    """, unsafe_allow_html=True)

    # TITLE
    st.markdown("""
    <div style="
        text-align:center;
        font-size:13px;
        font-weight:800;
        color:#ef4444;
        margin-bottom:10px;
    ">
        🚨 Overdue (>7 days)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # RISK BREAKDOWN (CLEAN LIST STYLE)
    # =========================
    st.markdown(f"""
    <div style="color:white; font-size:12.5px; line-height:1.8;">

        <div style="display:flex; justify-content:space-between;">
            <span>Total Overdue</span>
            <b>{overdue_total} ({overdue_pct}%)</b>
        </div>

        <div style="display:flex; justify-content:space-between; color:#f97316;">
            <span>TQ Overdue</span>
            <b>{overdue_tq} ({tq_pct}%)</b>
        </div>

        <div style="display:flex; justify-content:space-between; color:#38bdf8;">
            <span>RFI Overdue</span>
            <b>{overdue_rfi} ({rfi_pct}%)</b>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # CLOSE CARD
    st.markdown("</div>", unsafe_allow_html=True)
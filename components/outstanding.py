import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        st.warning("No data available")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    # =========================
    # TOTALS
    # =========================
    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    # =========================
    # OVERDUE (>7 DAYS)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1) if total else 0

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # SINGLE ALERT RECTANGLE
    # =========================
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #7f1d1d, #3b0a0a);
        border: 1px solid #ef4444;
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
        color: white;
        font-family: Arial;
    ">

        <!-- HEADER -->
        <div style="font-size:16px; font-weight:800; margin-bottom:12px;">
            🚨 Overdue (&gt;7 days)
        </div>

        <!-- OVERALL -->
        <div style="margin-bottom:12px;">
            <div style="font-size:28px; font-weight:900;">{overdue_total}</div>
            <div style="font-size:14px; color:#fecaca;">{overdue_pct}% of total</div>
        </div>

        <hr style="border:0; border-top:1px solid rgba(255,255,255,0.15); margin:10px 0;">

        <!-- TQ -->
        <div style="margin-bottom:10px;">
            <div style="font-size:14px; font-weight:700;">📌 TQ Overdue</div>
            <div style="font-size:20px; font-weight:800;">{overdue_tq}</div>
            <div style="font-size:13px; color:#fecaca;">{tq_pct}% of TQ total</div>
        </div>

        <!-- RFI -->
        <div>
            <div style="font-size:14px; font-weight:700;">📌 RFI Overdue</div>
            <div style="font-size:20px; font-weight:800;">{overdue_rfi}</div>
            <div style="font-size:13px; color:#fecaca;">{rfi_pct}% of RFI total</div>
        </div>

    </div>
    """, unsafe_allow_html=True)
    
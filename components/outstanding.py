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
    # TRUE RED RECTANGLE (NO CSS HACKS)
    # =========================
    col = st.columns([1])[0]

    with col:
        st.markdown(
            f"""
            <div style="
                background-color:#7f1d1d;
                border:2px solid #ef4444;
                border-radius:14px;
                padding:16px;
                color:white;
            ">
                <div style="font-size:18px; font-weight:800;">
                    🚨 Overdue (&gt;7 days)
                </div>

                <div style="margin-top:10px; font-size:28px; font-weight:900;">
                    {overdue_total}
                </div>
                <div style="font-size:13px; color:#fecaca;">
                    {overdue_pct}% of total
                </div>

                <hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin:10px 0;">

                <div style="font-size:14px;">
                    📌 TQ Overdue: <b>{overdue_tq}</b> ({tq_pct}%)
                </div>

                <div style="font-size:14px; margin-top:6px;">
                    📌 RFI Overdue: <b>{overdue_rfi}</b> ({rfi_pct}%)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
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
    # REAL RECTANGLE (STREAMLIT ONLY)
    # =========================
    box = st.container()

    with box:
        st.markdown("### 🚨 Overdue (>7 days)")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Overdue", overdue_total, f"{overdue_pct}%")

        with col2:
            st.metric("TQ Overdue", overdue_tq, f"{tq_pct}%")

        with col3:
            st.metric("RFI Overdue", overdue_rfi, f"{rfi_pct}%")

        # 👇 THIS IS WHAT CREATES THE "RECTANGLE FEEL"
        st.divider()
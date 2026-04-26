import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN DETECTION
    # =========================
    def find_col(name):
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
        return None

    status_col = find_col("status")
    doc_col = find_col("doc type")
    date_col = find_col("date sent")

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # LOGIC
    # =========================
    open_df = df[df[status_col] == "OPEN"]

    overdue_df = open_df[
        (today - open_df[date_col]).dt.days > 7
    ]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df[doc_col] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df[doc_col] == "RFI"])

    # =========================
    # SEVERITY
    # =========================
    if overdue_total >= 15:
        color = "red"
        status = "CRITICAL"
        impact = "High backlog risk"
    elif overdue_total >= 5:
        color = "orange"
        status = "HIGH"
        impact = "Needs attention"
    else:
        color = "gold"
        status = "MEDIUM"
        impact = "Monitor"

    # =========================
    # STREAMLIT CARD (NO HTML)
    # =========================
    with st.container():

        st.markdown(f"### 🚨 Outstanding Items (>7 Days) — {status}")

        st.caption(
            "Items are flagged when they are OPEN and exceed 7 days since Date Sent"
        )

        st.divider()

        # =========================
        # MAIN KPI
        # =========================
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.metric("Total Overdue", overdue_total, f"{overdue_pct}% of total")

        with col2:
            st.metric("TQ Overdue", overdue_tq)

        with col3:
            st.metric("RFI Overdue", overdue_rfi)

        # =========================
        # IMPACT LABEL
        # =========================
        st.markdown(f"**Status:** :{color}[{impact}]")

        st.divider()
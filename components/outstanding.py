import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN FIND
    # =========================
    def find_col(name):
        for c in df.columns:
            if c.strip().lower() == name.lower():
                return c
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
    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # LOGIC
    # =========================
    open_df = df[df[status_col] == "OPEN"]

    overdue_df = open_df[(today - open_df[date_col]).dt.days > 7]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df[doc_col] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df[doc_col] == "RFI"])

    # =========================
    # STATUS
    # =========================
    if overdue_total >= 15:
        status = "CRITICAL"
        color = "red"
    elif overdue_total >= 5:
        status = "HIGH"
        color = "orange"
    else:
        status = "MEDIUM"
        color = "green"

    # =========================
    # CARD
    # =========================
    with st.container(border=True):

        # HEADER (CARD TITLE)
        st.markdown(f"### 🚨 Outstanding Items (>7 Days)")

        st.caption("OPEN items older than 7 days since Date Sent are flagged as overdue")

        # BIG KPI (CENTRE PIECE)
        st.metric(
            label="Total Overdue Items",
            value=overdue_total,
            delta=f"{overdue_pct}% of total workload"
        )

        st.divider()

        # 2-COLUMN BREAKDOWN (CLEAN CARD STYLE)
        col1, col2 = st.columns(2)

        with col1:
            st.metric("TQ Overdue", overdue_tq)

        with col2:
            st.metric("RFI Overdue", overdue_rfi)

        # SPACING FOR CARD FEEL
        st.write("")

        # STATUS BOTTOM BLOCK (FINAL SUMMARY INSIDE CARD)
        st.metric("Status Level", status)
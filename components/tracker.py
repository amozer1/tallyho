import streamlit as st
import pandas as pd
from datetime import datetime


def render_tracker(df):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date", "status"]

    if not all(col in df.columns for col in required):
        st.error("Missing required columns in dataset")
        return

    # =========================
    # CLEAN DATA
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

    tq_pct = round(tq_total / total * 100, 1) if total else 0
    rfi_pct = round(rfi_total / total * 100, 1) if total else 0

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    overdue = len(df[df["age"] > 7])

    # =========================
    # TITLE
    # =========================
    st.markdown("## 📊 TQ & RFI Tracker Overview")

    left, right = st.columns([2, 1])

    # =========================
    # LEFT KPI SECTION
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                label="TOTAL TQ",
                value=tq_total,
                delta=f"{tq_pct}% of total"
            )

        with c2:
            st.metric(
                label="TOTAL RFI",
                value=rfi_total,
                delta=f"{rfi_pct}% of total"
            )

        with c3:
            st.metric(
                label="TOTAL (TQ + RFI)",
                value=combined_total,
                delta="100%"
            )

    # =========================
    # RIGHT CONTROL PANEL
    # =========================
    with right:

        st.markdown("### ⚙ Control Panel")

        st.metric("TQ not responded", tq_not)
        st.metric("RFI not responded", rfi_not)
        st.metric("Total not responded", total_not)

    # =========================
    # FOOTER RISK
    # =========================
    st.markdown("---")

    st.error(f"⚠ Outstanding > 7 Days: {overdue}")
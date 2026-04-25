import streamlit as st
import pandas as pd
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    # =========================
    # COUNTS
    # =========================
    tq_total = len(tq)
    rfi_total = len(rfi)
    combined = tq_total + rfi_total

    def split(data):
        open_ = data[data["reply date"].isna()]
        closed_ = data[data["reply date"].notna()]
        return open_, closed_

    tq_open, tq_closed = split(tq)
    rfi_open, rfi_closed = split(rfi)

    tq_open_n = len(tq_open)
    tq_closed_n = len(tq_closed)

    rfi_open_n = len(rfi_open)
    rfi_closed_n = len(rfi_closed)

    total_open = len(df[df["reply date"].isna()])
    total_closed = len(df[df["reply date"].notna()])

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # TITLE
    # =========================
    st.markdown("## 📊 TQ & RFI Control Room")

    # =========================
    # TOP KPI ROW
    # =========================
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.metric("TOTAL TQ", tq_total)

    with c2:
        with st.container(border=True):
            st.metric("TOTAL RFI", rfi_total)

    with c3:
        with st.container(border=True):
            st.metric("TOTAL WORK", combined)

    st.markdown("---")

    # =========================
    # TQ + RFI STATUS BLOCKS
    # =========================
    col1, col2 = st.columns(2)

    # ---------------- TQ ----------------
    with col1:
        with st.container(border=True):
            st.subheader("🔵 TQ STATUS")

            c1, c2, c3 = st.columns(3)

            c1.metric("OPEN", tq_open_n, f"{round(tq_open_n/tq_total*100,1) if tq_total else 0}%")
            c2.metric("CLOSED", tq_closed_n, f"{round(tq_closed_n/tq_total*100,1) if tq_total else 0}%")
            c3.metric("OUTSTANDING", tq_open_n, f"{round(tq_open_n/tq_total*100,1) if tq_total else 0}%")

    # ---------------- RFI ----------------
    with col2:
        with st.container(border=True):
            st.subheader("🟠 RFI STATUS")

            c1, c2, c3 = st.columns(3)

            c1.metric("OPEN", rfi_open_n, f"{round(rfi_open_n/rfi_total*100,1) if rfi_total else 0}%")
            c2.metric("CLOSED", rfi_closed_n, f"{round(rfi_closed_n/rfi_total*100,1) if rfi_total else 0}%")
            c3.metric("OUTSTANDING", rfi_open_n, f"{round(rfi_open_n/rfi_total*100,1) if rfi_total else 0}%")

    st.markdown("---")

    # =========================
    # OVERALL STATUS
    # =========================
    with st.container(border=True):
        st.subheader("📌 OVERALL STATUS")

        c1, c2, c3 = st.columns(3)

        c1.metric("OPEN", total_open, f"{round(total_open/total*100,1) if total else 0}%")
        c2.metric("CLOSED", total_closed, f"{round(total_closed/total*100,1) if total else 0}%")
        c3.metric("TOTAL", total)

    st.markdown("---")

    # =========================
    # RISK PANEL
    # =========================
    with st.container(border=True):
        st.subheader("⚠ OUTSTANDING RISK")

        st.error(f"OUTSTANDING > 7 DAYS: {overdue} ({round(overdue/total*100,1) if total else 0}%)")
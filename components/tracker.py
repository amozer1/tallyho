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

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

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

    overdue = len(df[(df["reply date"].isna()) & ((pd.Timestamp(datetime.today().date()) - df["date sent"]).dt.days > 7)])

    # =========================
    # COMPACT TITLE (SMALL FOOTPRINT)
    # =========================
    st.markdown("### 📊 TQ / RFI Tracker")

    # =========================
    # SINGLE KPI ROW (VERY COMPACT)
    # =========================
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("TQ", tq_total, f"{tq_open_n} open")

    with c2:
        st.metric("RFI", rfi_total, f"{rfi_open_n} open")

    with c3:
        st.metric("TOTAL", combined, f"{total_open} open")

    # =========================
    # MINI STATUS LINE (NO BLOCK HEIGHT GROWTH)
    # =========================
    st.markdown(
        f"""
        🔵 TQ Open: **{tq_open_n}** | Closed: **{tq_closed_n}**  
        🟠 RFI Open: **{rfi_open_n}** | Closed: **{rfi_closed_n}**
        """
    )

    # =========================
    # RISK STRIP (SMALL + SHARP)
    # =========================
    if overdue > 0:
        st.error(f"⚠ Overdue > 7 Days: {overdue}")
    else:
        st.success("✔ No overdue items")
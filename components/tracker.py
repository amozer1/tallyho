import streamlit as st
import pandas as pd
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date", "status"]

    if not all(c in df.columns for c in required):
        st.error("Missing required columns")
        return

    # =========================
    # DATA
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
    combined = tq_total + rfi_total

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
    # KPI BOX (STREAMLIT NATIVE)
    # =========================
    def kpi_box(value, label, pct, color):

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:10px;
                ">
                    <div style="font-size:38px;font-weight:700;color:{color};">
                        {value}
                    </div>

                    <div style="font-size:15px;margin-top:5px;font-weight:600;">
                        {label}
                    </div>

                    <div style="font-size:13px;color:gray;">
                        {pct}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================
    # LEFT KPIs
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_box(tq_total, "TOTAL TQ", f"{round(tq_total/total*100,1) if total else 0}%", "#3b82f6")

        with c2:
            kpi_box(rfi_total, "TOTAL RFI", f"{round(rfi_total/total*100,1) if total else 0}%", "#f59e0b")

        with c3:
            kpi_box(combined, "TQ + RFI", "100%", "#22c55e")

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("### ⚙ Control Panel")

        st.write(f"🔵 TQ not responded: **{tq_not}** ({round(tq_not/tq_total*100,1) if tq_total else 0}%)")
        st.write(f"🟠 RFI not responded: **{rfi_not}** ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)")
        st.write(f"⚫ Total not responded: **{total_not}** ({round(total_not/total*100,1) if total else 0}%)")

    # =========================
    # FOOTER
    # =========================
    st.markdown("---")

    st.error(f"⚠ Outstanding > 7 Days: {overdue} ({round(overdue/total*100,1) if total else 0}%)")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_venn_overview(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # =========================
    REQUIRED COLUMNS
    # =========================
    required = ["doc type", "date sent", "reply date", "status"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    DATE HANDLING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    # =========================
    TYPE SPLIT
    # =========================
    tq = df[df["doc type"] == "tq"]
    rfi = df[df["doc type"] == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    # =========================
    NOT RESPONDED
    # =========================
    tq_not_resp = len(tq[tq["reply date"].isna()])
    rfi_not_resp = len(rfi[rfi["reply date"].isna()])
    total_not_resp = len(df[df["reply date"].isna()])

    # =========================
    OUTSTANDING (>7 DAYS)
    # =========================
    outstanding = df[df["age"] > 7]
    outstanding_count = len(outstanding)

    # =========================
    HEADER
    # =========================
    st.markdown("### 🧭 TQ & RFI Controls Tracker")

    # =========================
    MAIN LAYOUT
    # =========================
    left, right = st.columns([1.6, 1])

    # =========================
    LEFT: 3 CIRCLES (DONUTS)
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        # ---- TQ ----
        with c1:
            fig1 = go.Figure(go.Pie(
                values=[tq_total],
                labels=["TQ"],
                hole=0.7,
                marker=dict(colors=["#4da3ff"])
            ))
            fig1.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(f"**TQ Total:** {tq_total} ({round(tq_total/total*100,1)}%)")

        # ---- RFI ----
        with c2:
            fig2 = go.Figure(go.Pie(
                values=[rfi_total],
                labels=["RFI"],
                hole=0.7,
                marker=dict(colors=["#fbbf24"])
            ))
            fig2.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(f"**RFI Total:** {rfi_total} ({round(rfi_total/total*100,1)}%)")

        # ---- TOTAL ----
        with c3:
            fig3 = go.Figure(go.Pie(
                values=[total],
                labels=["Total"],
                hole=0.7,
                marker=dict(colors=["#22c55e"])
            ))
            fig3.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(f"**Total:** {total} (100%)")

    # =========================
    # RIGHT: CONTROL PANEL
    # =========================
    with right:

        st.markdown("#### Not Responded Summary")

        st.markdown(f"""
- 🔵 TQ not responded: **{tq_not_resp} ({round(tq_not_resp/tq_total*100 if tq_total else 0,1)}%)**
- 🟠 RFI not responded: **{rfi_not_resp} ({round(rfi_not_resp/rfi_total*100 if rfi_total else 0,1)}%)**
- ⚫ Total not responded: **{total_not_resp} ({round(total_not_resp/total*100 if total else 0,1)}%)**
""")

        st.markdown("---")

        st.markdown(f"""
### ⚠ Outstanding (>7 days)

**{outstanding_count} ({round(outstanding_count/total*100 if total else 0,1)}%)**

> Items exceeding 7 days without closure or response are flagged as operational risk.
""")
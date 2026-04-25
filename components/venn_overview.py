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

    required = ["doc type", "date sent", "reply date", "status"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # DATE PROCESSING
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    # =========================
    # SPLIT DATA
    # =========================
    tq = df[df["doc type"] == "tq"]
    rfi = df[df["doc type"] == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)
    combined_total = tq_total + rfi_total

    # =========================
    # NOT RESPONDED
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    # =========================
    # OUTSTANDING
    # =========================
    overdue = df[df["age"] > 7]
    overdue_count = len(overdue)

    # =========================
    # HEADER
    # =========================
    st.markdown(
        """
        <h2 style="
            text-align:center;
            font-weight:800;
            background: linear-gradient(90deg, #4da3ff, #a855f7, #22c55e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">
        TQ / RFI Intelligence Control Dashboard
        </h2>
        <hr style="border:1px solid #eee">
        """,
        unsafe_allow_html=True
    )

    # =========================
    # LAYOUT
    # =========================
    left, right = st.columns([1.6, 1])

    # =========================
    # LEFT: 3 KPI CIRCLES
    # =========================
    with left:

        c1, c2, c3 = st.columns(3)

        # ---- TQ ----
        with c1:
            fig = go.Figure(go.Pie(
                values=[tq_total],
                labels=["TQ"],
                hole=0.65,
                marker=dict(colors=["#4da3ff"])
            ))
            fig.update_layout(height=220, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style="text-align:center;padding:8px;">
                <b>Total TQ</b><br>
                {tq_total} ({round(tq_total/total*100,1) if total else 0}%)
            </div>
            """, unsafe_allow_html=True)

        # ---- RFI ----
        with c2:
            fig = go.Figure(go.Pie(
                values=[rfi_total],
                labels=["RFI"],
                hole=0.65,
                marker=dict(colors=["#fbbf24"])
            ))
            fig.update_layout(height=220, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style="text-align:center;padding:8px;">
                <b>Total RFI</b><br>
                {rfi_total} ({round(rfi_total/total*100,1) if total else 0}%)
            </div>
            """, unsafe_allow_html=True)

        # ---- COMBINED ----
        with c3:
            fig = go.Figure(go.Pie(
                values=[combined_total],
                labels=["Combined"],
                hole=0.65,
                marker=dict(colors=["#22c55e"])
            ))
            fig.update_layout(height=220, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style="text-align:center;padding:8px;">
                <b>Total Workload</b><br>
                {combined_total} (100%)
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # RIGHT: CONTROL PANEL
    # =========================
    with right:

        st.markdown("### Control & Response Intelligence")

        st.markdown(f"""
        <div style="
            padding:15px;
            border-radius:12px;
            border:1px solid #eee;
            background:#fafafa;
        ">

        🔵 <b>TQs not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br><br>

        🟠 <b>RFIs not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br><br>

        ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)

        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div style="
            padding:12px;
            border-radius:12px;
            border-left:5px solid #ef4444;
            background:#fff5f5;
        ">
        ⚠ <b>Outstanding > 7 Days:</b><br>
        {overdue_count} ({round(overdue_count/total*100,1) if total else 0}%)
        </div>
        """, unsafe_allow_html=True)
        
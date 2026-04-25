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

    tq = df[df["doc type"] == "tq"]
    rfi = df[df["doc type"] == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    # BOTH (intersection logic approximation = duplicate or linked records placeholder)
    both_total = len(df[(df["doc type"].isin(["tq", "rfi"]))])

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

    # =========================================================
    # LAYOUT
    # =========================================================
    left, right = st.columns([1.6, 1])

    # =========================================================
    # 🟦 LEFT: 3 CIRCLES (VENN STYLE VISUAL)
    # =========================================================
    with left:

        c1, c2, c3 = st.columns(3)

        # -------------------------
        # TQ CIRCLE
        # -------------------------
        with c1:
            fig = go.Figure(go.Pie(
                values=[tq_total, total - tq_total],
                hole=0.72,
                marker=dict(colors=["#4da3ff", "#f3f4f6"]),
                textinfo="none"
            ))
            fig.update_layout(height=250, showlegend=False, margin=dict(t=10, b=10))

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f"""
                <div style="text-align:center">
                    <b>Total TQ</b><br>
                    {tq_total} ({round(tq_total/total*100,1) if total else 0}%)
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------
        # BOTH / OVERLAP CIRCLE
        # -------------------------
        with c2:
            fig = go.Figure(go.Pie(
                values=[both_total, total - both_total],
                hole=0.65,
                marker=dict(colors=["#22c55e", "#f3f4f6"]),
                textinfo="none"
            ))
            fig.update_layout(height=280, showlegend=False, margin=dict(t=10, b=10))

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f"""
                <div style="text-align:center">
                    <b>TQ & RFI (Combined)</b><br>
                    {both_total} ({round(both_total/total*100,1) if total else 0}%)
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------
        # RFI CIRCLE
        # -------------------------
        with c3:
            fig = go.Figure(go.Pie(
                values=[rfi_total, total - rfi_total],
                hole=0.72,
                marker=dict(colors=["#fbbf24", "#f3f4f6"]),
                textinfo="none"
            ))
            fig.update_layout(height=250, showlegend=False, margin=dict(t=10, b=10))

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f"""
                <div style="text-align:center">
                    <b>Total RFI</b><br>
                    {rfi_total} ({round(rfi_total/total*100,1) if total else 0}%)
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================================================
    # 🟪 RIGHT: CONTROL PANEL BOX
    # =========================================================
    with right:

        st.markdown(f"""
        <div style="
            padding:16px;
            border-radius:12px;
            border:1px solid #eee;
            background:#fafafa;
        ">

        <h4>Response Overview</h4>

        🔵 <b>TQ not responded:</b> {tq_not} ({round(tq_not/tq_total*100,1) if tq_total else 0}%)<br><br>

        🟠 <b>RFI not responded:</b> {rfi_not} ({round(rfi_not/rfi_total*100,1) if rfi_total else 0}%)<br><br>

        ⚫ <b>Total not responded:</b> {total_not} ({round(total_not/total*100,1) if total else 0}%)

        </div>
        """, unsafe_allow_html=True)

    # =========================================================
    # 🟥 OUTSTANDING BOX (BOTTOM)
    # =========================================================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        padding:14px;
        border-radius:10px;
        border-left:6px solid #ef4444;
        background:#fff5f5;
    ">
    ⚠ <b>Outstanding > 7 Days:</b> {overdue_count} ({round(overdue_count/total*100,1) if total else 0}%)
    </div>
    """, unsafe_allow_html=True)
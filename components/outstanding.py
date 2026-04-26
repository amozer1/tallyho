import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN FIND
    # =========================
    def col(name):
        for c in df.columns:
            if c.strip().lower() == name.lower():
                return c
        return None

    status_col = col("status")
    doc_col = col("doc type")
    date_col = col("date sent")

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
        color = "#ef4444"
    elif overdue_total >= 5:
        status = "HIGH"
        color = "#f97316"
    else:
        status = "MEDIUM"
        color = "#facc15"

    # =========================
    # CENTERED CARD
    # =========================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # =========================
        # HEADER (NO DUPLICATION HERE)
        # =========================
        st.markdown(f"### 🚨 Outstanding (>7 Days) — {status}")

        # =========================
        # NOTE (INSIDE CARD, CLEAN)
        # =========================
        st.caption(
            "Overdue = OPEN items where (Today - Date Sent) > 7 days"
        )

        # =========================
        # KPI ROW (SINGLE SOURCE OF TRUTH)
        # =========================
        k1, k2, k3 = st.columns(3)

        with k1:
            st.metric("Overdue", overdue_total, f"{overdue_pct}%")

        with k2:
            st.metric("TQ", overdue_tq)

        with k3:
            st.metric("RFI", overdue_rfi)

        # =========================
        # VISUAL (SIMPLE + NON-REDUNDANT)
        # =========================
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["TQ", "RFI"],
            values=[overdue_tq, overdue_rfi],
            hole=0.55,
            marker=dict(colors=["#f97316", "#38bdf8"]),
            textinfo="label+value"
        ))

        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
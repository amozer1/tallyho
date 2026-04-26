import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN DETECTION
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
        status = "CRITICAL"
        color = "#ef4444"
    elif overdue_total >= 5:
        status = "HIGH"
        color = "#f97316"
    else:
        status = "MEDIUM"
        color = "#facc15"

    # =========================
    # CENTERED CARD (LIKE AGE MODULE)
    # =========================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # =========================
        # HEADER (COMPACT)
        # =========================
        st.markdown(
            f"## 🚨 Outstanding (>7 Days) — {status}\n"
            f"**Overdue:** {overdue_total} ({overdue_pct}%) "
            f"· **TQ:** {overdue_tq} "
            f"· **RFI:** {overdue_rfi}"
        )

        # =========================
        # DONUT CHART (NO DUPLICATION)
        # =========================
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["TQ Overdue", "RFI Overdue"],
            values=[overdue_tq, overdue_rfi],
            hole=0.55,
            marker=dict(colors=["#f97316", "#38bdf8"]),
            textinfo="label+value",
            hovertemplate="%{label}: %{value}<extra></extra>"
        ))

        fig.update_layout(
            height=240,
            margin=dict(l=20, r=20, t=10, b=10),
            paper_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    # =========================
    # OVERDUE (>7 DAYS)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # SEVERITY LOGIC
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        label = "CRITICAL"
        impact = "High risk to project progress"
    elif overdue_total >= 5:
        color = "#f97316"
        label = "HIGH"
        impact = "Moderate impact on workflow"
    else:
        color = "#facc15"
        label = "MEDIUM"
        impact = "Monitor backlog"

    # =========================
    # TITLE
    # =========================
    st.markdown("### 🚨 Outstanding (>7 days)")

    st.caption(f"Status: {label} | {impact}")

    # =========================
    # MAIN KPI ROW
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Overdue",
            overdue_total,
            f"{overdue_pct}%"
        )

    with col2:
        st.metric(
            "TQ Overdue",
            overdue_tq,
            f"{tq_pct}%"
        )

    with col3:
        st.metric(
            "RFI Overdue",
            overdue_rfi,
            f"{rfi_pct}%"
        )

    # =========================
    # IMPACT FOOTNOTE
    # =========================
    st.markdown(
        f"**Impact:** {impact}",
        help="This indicates the operational risk level of overdue items."
    )
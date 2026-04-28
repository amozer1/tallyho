import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # FIND COLUMNS
    # =========================
    status_col = next((c for c in df.columns if c.lower() == "status"), None)
    doc_col = next((c for c in df.columns if c.lower() == "doc type"), None)
    date_col = next((c for c in df.columns if c.lower() == "date sent"), None)

    if not status_col or not doc_col or not date_col:
        st.error("Required columns missing.")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA
    # =========================
    tq_df = df[df[doc_col] == "TQ"]
    rfi_df = df[df[doc_col] == "RFI"]

    def get_counts(sub_df):
        open_items = len(sub_df[sub_df[status_col] == "OPEN"])
        closed_items = len(sub_df[sub_df[status_col] == "CLOSED"])
        overdue_items = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )
        return open_items, closed_items, overdue_items

    tq_open, tq_closed, tq_overdue = get_counts(tq_df)
    rfi_open, rfi_closed, rfi_overdue = get_counts(rfi_df)

    overdue_total = tq_overdue + rfi_overdue
    overdue_pct = round((overdue_total / total) * 100, 1)

    # =========================
    # SEVERITY
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
    else:
        color = "#facc15"
        status = "MEDIUM"

    # =========================
    # HEADER
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:{color};
    ">
        🚨 Outstanding (>14 Days) — {status}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI
    # =========================
    st.metric("Total Outstanding", overdue_total, f"{overdue_pct}% of total")

    # =========================
    # PIE CHARTS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        fig_tq = go.Figure(data=[go.Pie(
            labels=["Open", "Closed", "Outstanding"],
            values=[tq_open, tq_closed, tq_overdue],
            hole=0.55,
            marker=dict(colors=["#38bdf8", "#22c55e", "#f97316"]),
            textinfo="label+value"
        )])

        fig_tq.update_layout(
            title="TQ Status",
            height=300,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white")
        )

        st.plotly_chart(fig_tq, use_container_width=True)

    with col2:
        fig_rfi = go.Figure(data=[go.Pie(
            labels=["Open", "Closed", "Outstanding"],
            values=[rfi_open, rfi_closed, rfi_overdue],
            hole=0.55,
            marker=dict(colors=["#38bdf8", "#22c55e", "#f97316"]),
            textinfo="label+value"
        )])

        fig_rfi.update_layout(
            title="RFI Status",
            height=300,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white")
        )

        st.plotly_chart(fig_rfi, use_container_width=True)

    # =========================
    # FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:4px;
        text-align:center;
    ">
        TQ Outstanding: {tq_overdue} | RFI Outstanding: {rfi_overdue}
    </div>
    """, unsafe_allow_html=True)
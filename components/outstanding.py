import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN FINDING
    # =========================
    def find_col(name):
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
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

    total_tq = len(df[df[doc_col] == "TQ"])
    total_rfi = len(df[df[doc_col] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # STATUS
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
        impact = "High backlog risk"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
    else:
        color = "#facc15"
        status = "MEDIUM"

    # =========================
    # HEADER (SAFE HTML ONLY)
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:10px;
        text-align:center;
        color:{color};
        font-weight:700;
        font-size:13px;
    ">
        🚨 Outstanding (>7 Days) — {status}
        <div style="
            font-size:11px;
            color:#94a3b8;
            font-weight:400;
            margin-top:4px;
        ">
            OPEN items older than 7 days since Date Sent are flagged as overdue
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI SECTION (STREAMLIT SAFE)
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("Overdue", overdue_total, f"{overdue_pct}%")
    col2.metric("TQ Overdue", overdue_tq)
    col3.metric("RFI Overdue", overdue_rfi)

    st.markdown(
        f"<div style='color:#94a3b8;font-size:12px;margin-top:-5px;'>Status: <b style='color:{color}'>{impact}</b></div>",
        unsafe_allow_html=True
    )

    # =========================
    # CHART (STREAMLIT SAFE)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ", "RFI"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"]),
        text=[overdue_tq, overdue_rfi],
        textposition="auto"
    ))

    fig.update_layout(
        height=160,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)
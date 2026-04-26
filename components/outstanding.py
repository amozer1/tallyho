import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    df.columns = df.columns.str.strip()

    def find_col(name):
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
        return None

    status_col = find_col("Status")
    doc_col = find_col("doc type")
    date_col = find_col("date sent")

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns")
        st.write(df.columns.tolist())
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
        impact = "Needs attention"
    else:
        color = "#facc15"
        status = "MEDIUM"
        impact = "Monitor"

    # =========================
    # BUILD CHART (AS HTML IMAGE)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ Overdue", "RFI Overdue"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"]),
        text=[f"{overdue_tq}", f"{overdue_rfi}"],
        textposition="auto"
    ))

    fig.update_layout(
        height=160,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # =========================
    # SINGLE UNIFIED CARD
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:14px;
    ">

        <!-- HEADER -->
        <div style="
            text-align:center;
            font-size:14px;
            font-weight:800;
            color:{color};
        ">
            🚨 Outstanding (>7 Days) — {status}
        </div>

        <!-- NOTE -->
        <div style="
            text-align:center;
            font-size:11px;
            color:#94a3b8;
            margin-top:6px;
            margin-bottom:10px;
        ">
            Items are <b>Overdue</b> when they are <b>OPEN</b> and exceed <b>7 days since Date Sent</b>.
        </div>

        <!-- KPI ROW -->
        <div style="
            display:flex;
            justify-content:space-between;
            margin-bottom:10px;
            font-size:12px;
        ">
            <div style="color:white;">
                <b>{overdue_total}</b><br>
                <span style="color:#94a3b8;">Overdue</span>
            </div>

            <div style="color:{color}; font-weight:700;">
                {impact}<br>
                <span style="color:#94a3b8; font-weight:400;">Status</span>
            </div>

            <div style="color:#cbd5e1;">
                TQ: {overdue_tq} | RFI: {overdue_rfi}
            </div>
        </div>

        <!-- CHART -->
        <div>
            {chart_html}
        </div>

    </div>
    """, unsafe_allow_html=True)
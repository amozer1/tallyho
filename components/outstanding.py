import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["Status"] = df["Status"].astype(str).str.strip().str.upper()

    df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # CORE LOGIC (NEW SLA MODEL)
    # =========================

    # 🔴 OPEN ITEMS
    open_df = df[df["Status"] == "OPEN"]

    # 🚨 OVERDUE = OPEN + > 7 days since sent
    overdue_df = open_df[
        (today - open_df["Date Sent"]).dt.days > 7
    ]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    # =========================
    # BREAKDOWN
    # =========================
    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # =========================
    # SEVERITY ENGINE
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
    # HEADER
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:6px 10px;
        margin-bottom:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:{color};
    ">
        🚨 Outstanding (>7 Days SLA) — {status}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI ROW
    # =========================
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.metric(
            label="Total Overdue (SLA Breach)",
            value=f"{overdue_total}",
            delta=f"{overdue_pct}% of total"
        )

    with col2:
        st.markdown(f"""
        <div style="padding-top:6px;">
            <div style="font-size:12px; font-weight:700; color:{color};">
                {impact}
            </div>
            <div style="font-size:11px; color:#cbd5e1;">
                TQ: {overdue_tq} | RFI: {overdue_rfi}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # BAR CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[overdue_tq, overdue_rfi],
        y=["TQ Overdue", "RFI Overdue"],
        orientation="h",
        marker=dict(color=["#f97316", "#38bdf8"]),
        text=[
            f"{overdue_tq} ({tq_pct}%)",
            f"{overdue_rfi} ({rfi_pct}%)"
        ],
        textposition="outside"
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=15, r=15, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:2px;
    ">
        Status: <span style="color:{color}; font-weight:600;">{impact}</span>
    </div>
    """, unsafe_allow_html=True)
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMNS
    # =========================
    df.columns = df.columns.str.strip()

    # =========================
    # FIND COLUMNS SAFELY
    # =========================
    def find_col(name):
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
        return None

    status_col = find_col("Status")
    doc_col = find_col("doc type")
    date_col = find_col("date sent")

    if not status_col or not doc_col or not date_col:
        st.error("❌ Missing required columns (Status / Doc Type / Date Sent)")
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
    # STATUS LEVEL
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
    # FULL CARD
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:12px 14px;
        margin-top:8px;
        margin-bottom:8px;
    ">

        <!-- HEADER -->
        <div style="
            text-align:center;
            font-size:13px;
            font-weight:800;
            color:{color};
            margin-bottom:6px;
        ">
            🚨 Outstanding (>7 Days) — {status}
        </div>

        <!-- NOTE -->
        <div style="
            text-align:center;
            font-size:11px;
            color:#94a3b8;
            margin-bottom:10px;
            line-height:1.4;
        ">
            Items are <b>Overdue</b> when they are <b>OPEN</b> and have been outstanding for more than <b>7 days since Date Sent</b>.
        </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI + TEXT INSIDE CARD (STREAMLIT SECTION)
    # =========================
    with st.container():

        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.metric(
                label="Total Overdue",
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
    # CHART (STILL VISUALLY LINKED TO CARD)
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
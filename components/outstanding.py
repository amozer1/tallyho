import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # SAFE COLUMN DETECTION
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
        st.error("Missing required columns: Status / Doc Type / Date Sent")
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
    # CARD UI
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:14px;
        padding:16px;
        margin-top:10px;
    ">

        <!-- HEADER -->
        <div style="
            text-align:center;
            font-size:14px;
            font-weight:800;
            color:{color};
            margin-bottom:6px;
        ">
            🚨 Outstanding Items (>7 Days) — {status}
        </div>

        <!-- RULE -->
        <div style="
            text-align:center;
            font-size:11px;
            color:#94a3b8;
            margin-bottom:14px;
            line-height:1.4;
        ">
            Items are flagged when they are <b>OPEN</b> and exceed <b>7 days since Date Sent</b>
        </div>

        <!-- MAIN KPI -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:14px;
        ">
            <div style="text-align:left;">
                <div style="font-size:22px; font-weight:800; color:white;">
                    {overdue_total}
                </div>
                <div style="font-size:11px; color:#94a3b8;">
                    Total Overdue ({overdue_pct}%)
                </div>
            </div>

            <div style="
                text-align:right;
                font-size:12px;
                color:{color};
                font-weight:700;
            ">
                {impact}
            </div>
        </div>

        <!-- BREAKDOWN -->
        <div style="
            display:flex;
            justify-content:space-between;
            border-top:1px solid #1f2937;
            padding-top:10px;
            font-size:12px;
        ">
            <div style="color:#38bdf8;">
                TQ Overdue: <b>{overdue_tq}</b>
            </div>

            <div style="color:#f97316;">
                RFI Overdue: <b>{overdue_rfi}</b>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)
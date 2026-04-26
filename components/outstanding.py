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
    # IMPACT LOGIC (NEW)
    # =========================
    if overdue_total >= 15:
        severity = "critical"
        impact_line = "High impact on project delivery"
        sub_line = "May block approvals & coordination"
        color = "#ef4444"
    elif overdue_total >= 5:
        severity = "high"
        impact_line = "Moderate impact on progress"
        sub_line = "Attention required"
        color = "#f97316"
    else:
        severity = "low"
        impact_line = "Low backlog risk"
        sub_line = "Monitor"
        color = "#f59e0b"

    # =========================
    # CARD CONTAINER
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:14px;
        padding:14px;
        height:230px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    ">
    """, unsafe_allow_html=True)

    # =========================
    # TITLE (URGENT KPI HEADER)
    # =========================
    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:13px;
        font-weight:900;
        color:{color};
        margin-bottom:8px;
        letter-spacing:0.5px;
    ">
        🚨 OVERDUE (>7 DAYS)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # MAIN KPI (HERO)
    # =========================
    st.markdown(f"""
    <div style="
        text-align:center;
        margin-bottom:10px;
    ">
        <div style="font-size:28px; font-weight:800; color:white; line-height:1;">
            {overdue_total}
        </div>
        <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
            {overdue_pct}% of total documents
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # ACTION LINES (NEW MEANING LAYER)
    # =========================
    st.markdown(f"""
    <div style="
        font-size:12.5px;
        color:white;
        line-height:1.6;
        margin-top:6px;
    ">

        <div style="display:flex; justify-content:space-between;">
            <span>Total Overdue</span>
            <b>{overdue_total} ({overdue_pct}%)</b>
        </div>

        <div style="display:flex; justify-content:space-between; color:#f97316;">
            <span>TQ Overdue</span>
            <b>{overdue_tq} ({tq_pct}%)</b>
        </div>

        <div style="display:flex; justify-content:space-between; color:#38bdf8;">
            <span>RFI Overdue</span>
            <b>{overdue_rfi} ({rfi_pct}%)</b>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # IMPACT / CONSEQUENCE LAYER (NEW)
    # =========================
    st.markdown(f"""
    <div style="
        margin-top:10px;
        padding-top:8px;
        border-top:1px solid #1f2937;
        font-size:12px;
    ">
        <div style="color:{color}; font-weight:700;">
            {impact_line}
        </div>
        <div style="color:#cbd5e1; margin-top:2px;">
            {sub_line}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CLOSE CARD
    st.markdown("</div>", unsafe_allow_html=True)
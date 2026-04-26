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
    # SEVERITY (COMPACT)
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        label = "CRITICAL"
    elif overdue_total >= 5:
        color = "#f97316"
        label = "HIGH"
    else:
        color = "#facc15"
        label = "MEDIUM"

    # =========================
    # HEADER (SMALL)
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
        font-weight:800;
        color:{color};
    ">
        🚨 OVERDUE ({label})
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI ROW (COMPACT)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total", overdue_total, f"{overdue_pct}%")

    with col2:
        st.metric("TQ", overdue_tq, f"{tq_pct}%")

    with col3:
        st.metric("RFI", overdue_rfi, f"{rfi_pct}%")

    # =========================
    # FOOTER (MINIMAL IMPACT)
    # =========================
    impact = (
        "High impact on progress" if overdue_total >= 15
        else "Monitor backlog"
    )

    st.markdown(f"""
    <div style="
        font-size:11.5px;
        color:#cbd5e1;
        margin-top:4px;
        text-align:center;
    ">
        <span style="color:{color}; font-weight:700;">
            {impact}
        </span>
    </div>
    """, unsafe_allow_html=True)
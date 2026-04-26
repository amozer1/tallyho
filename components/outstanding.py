import pandas as pd
import streamlit as st


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    # OPEN CARD
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:8px 10px;
        margin-bottom:6px;
    ">
        <div style="
            text-align:center;
            font-size:13px;
            font-weight:800;
            color:#ef4444;
            margin-bottom:10px;
        ">
            🚨 Critical Alert: Overdue Items (>7 days)
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Overdue Total", overdue_total, f"{overdue_pct}%")

    with c2:
        st.metric("TQ Overdue", overdue_tq, f"{tq_pct}%")

    with c3:
        st.metric("RFI Overdue", overdue_rfi, f"{rfi_pct}%")

    # CLOSE CARD
    st.markdown("</div>", unsafe_allow_html=True)
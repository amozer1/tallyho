import pandas as pd
import streamlit as st


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div style="
        text-align:center;
        font-size:14px;
        font-weight:800;
        color:#E2E8F0;
        margin-bottom:10px;
    ">
        📊 TQ / RFI Control Panel
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CSS CIRCLE STYLE
    # =========================
    st.markdown("""
    <style>
    .kpi-row {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }

    .kpi-card {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: 700;
        text-align: center;
    }

    .tq { background: rgba(59,130,246,0.25); border:2px solid #60A5FA; }
    .total { background: rgba(168,85,247,0.25); border:2px solid #A855F7; }
    .rfi { background: rgba(34,197,94,0.25); border:2px solid #4ADE80; }

    .small {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # KPI CARDS
    # =========================
    st.markdown(f"""
    <div class="kpi-row">

        <div class="kpi-card">
            <div class="circle tq">
                <div>TQ Only</div>
                <div style="font-size:20px;">{tq_pct}%</div>
                <div style="font-size:24px;">{tq_total}</div>
                <div class="small">Not: {tq_not}</div>
            </div>
        </div>

        <div class="kpi-card">
            <div class="circle total">
                <div>TQ + RFI</div>
                <div style="font-size:20px;">100%</div>
                <div style="font-size:24px;">{total}</div>
                <div class="small">Not: {total_not}</div>
            </div>
        </div>

        <div class="kpi-card">
            <div class="circle rfi">
                <div>RFI Only</div>
                <div style="font-size:20px;">{rfi_pct}%</div>
                <div style="font-size:24px;">{rfi_total}</div>
                <div class="small">Not: {rfi_not}</div>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# =========================
# CARD WRAPPER (ONLY IF NOT IN SHARED FILE)
# =========================
def render_card(title, subtitle=None):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 18px 10px 18px;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    ">
        <div style="font-size:18px; font-weight:700; color:white;">
            {title}
        </div>
        <div style="font-size:13px; color:#9ca3af; margin-top:2px;">
            {subtitle or ""}
        </div>
    """, unsafe_allow_html=True)


def end_card():
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN TRACKER
# =========================
def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # SAFE CLEANING
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.lower().str.strip()

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    df = df[df["age"].notna()]

    total = len(df)

    # =========================
    # SPLIT
    # =========================
    tq = df[df["doc type"] == "tq"]
    rfi = df[df["doc type"] == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # NOT RESPONDED
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

    # =========================
    # OVERDUE
    # =========================
    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # CARD START
    # =========================
    render_card(
        "TQ & RFI Intelligence Hub",
        "Project Controls • Response Analytics • Document Tracking"
    )

    # =========================
    # LAYOUT
    # =========================
    left, right = st.columns([1, 1])

    with left:
        fig = go.Figure()

        # =====================================================
        # YOUR ORIGINAL FIGURE CODE GOES HERE (UNCHANGED)
        # =====================================================
        # keep all shapes, annotations, layout exactly as before

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("")

    # =========================
    # END CARD
    # =========================
    end_card()
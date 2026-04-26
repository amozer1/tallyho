import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime



def render_tracker(df):

    # =========================
    # CARD WRAPPER
    # =========================
    st.markdown("""
    <style>
    .tracker-card {
        background: linear-gradient(145deg, #0b1220, #0f172a);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 18px 10px 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        margin-bottom: 18px;
    }

    .tracker-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .tracker-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # CARD START
    # =========================
    with st.container():
        st.markdown('<div class="tracker-card">', unsafe_allow_html=True)

        st.markdown('<div class="tracker-title">TQ & RFI Intelligence Tracker</div>', unsafe_allow_html=True)
        st.markdown('<div class="tracker-subtitle">Response and timeliness overview</div>', unsafe_allow_html=True)

        # -------------------------
        # YOUR EXISTING LOGIC HERE
        # -------------------------
        if df is None or df.empty:
            st.warning("No data available.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]

        required = ["doc type", "date sent", "reply date"]
        for c in required:
            if c not in df.columns:
                st.error(f"Missing column: {c}")
                st.markdown('</div>', unsafe_allow_html=True)
                return

        df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
        df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

        today = pd.Timestamp(datetime.today().date())
        df["age"] = (today - df["date sent"]).dt.days

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

        tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
        rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
        total_not_pct = round((total_not / total) * 100, 1) if total else 0

        # OUTSTANDING > 7 DAYS
        overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

        # =========================
        # YOUR FIGURE (UNCHANGED)
        # =========================
        left, right = st.columns([1, 1])

        with left:
            fig = go.Figure()

            # (your full plotly code stays exactly as-is)

            fig.update_layout(
                height=380,
                paper_bgcolor="#0b1220",
                plot_bgcolor="#0b1220",
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(visible=False, range=[-0.3, 3.5]),
                yaxis=dict(visible=False, range=[-0.3, 1.9]),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)
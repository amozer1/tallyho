import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    .block-container {
        padding-top: 0rem !important;
    }

    /* ===============================
       MAIN CONTINUOUS HEADER BAR
    =============================== */
    .header-bar {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        border-radius: 18px;

        padding: 16px 20px;
        margin-bottom: 12px;

        box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
    }

    /* ===============================
       INNER "CARD" SECTIONS
    =============================== */
    .card-section {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;

        padding: 12px 14px;
    }

    /* TITLE */
    .title {
        font-size: 26px;
        font-weight: 900;
        color: white;
        line-height: 1.1;
    }

    .subtitle {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* STATUS PILL */
    .status {
        display: inline-flex;
        align-items: center;
        gap: 6px;

        padding: 8px 12px;
        border-radius: 10px;

        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);

        color: white;
        font-size: 13px;
        font-weight: 700;

        white-space: nowrap;
    }

    .dot {
        color: #22c55e;
        font-size: 16px;
    }

    /* DATE */
    .date {
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-align: right;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= HEADER BAR =================
    with st.container():
        st.markdown('<div class="header-bar">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([5, 2, 2], vertical_alignment="center")

        # LEFT (CARD INSIDE HEADER)
        with col1:
            st.markdown('<div class="card-section">', unsafe_allow_html=True)
            st.markdown('<div class="title">Tally Ho TQ & RFI Tracker</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtitle">TQs • RFIs • Outstanding Responses</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # CENTER (STATUS CARD)
        with col2:
            st.markdown('<div class="card-section" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown('<div class="status"><span class="dot">●</span>Live System Status: Active</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # RIGHT (DATE CARD)
        with col3:
            st.markdown('<div class="card-section" style="text-align:right;">', unsafe_allow_html=True)
            st.markdown(f'<div class="date">{datetime.today().strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
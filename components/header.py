import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem !important;
        }

        /* HEADER CARD */
        .header-card {
            background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
            border: 1px solid rgba(122, 60, 255, 0.18);
            border-radius: 16px;
            padding: 18px 22px;

            box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
        }

        /* TITLE */
        .header-title {
            font-size: 26px;
            font-weight: 900;
            color: white;
            margin-bottom: 4px;
            line-height: 1.1;
        }

        /* SUBTITLE */
        .header-subtitle {
            font-size: 12px;
            color: #94a3b8;
        }

        /* STATUS PILL */
        .status-pill {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 10px;

            background: rgba(122, 60, 255, 0.12);
            border: 1px solid rgba(122, 60, 255, 0.25);

            color: white;
            font-size: 13px;
            font-weight: 700;
        }

        .dot {
            color: #22c55e;
            margin-right: 6px;
        }

        /* DATE */
        .date-text {
            color: white;
            font-size: 14px;
            font-weight: 700;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

    # CARD
    with st.container():

        st.markdown('<div class="header-card">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([5, 2, 2])

        # LEFT
        with col1:
            st.markdown('<div class="header-title">Tally Ho TQ & RFI Tracker</div>', unsafe_allow_html=True)
            st.markdown('<div class="header-subtitle">TQs • RFIs • Outstanding Responses</div>', unsafe_allow_html=True)

        # CENTER
        with col2:
            st.markdown('<div class="status-pill"><span class="dot">●</span>Live System Status: Active</div>', unsafe_allow_html=True)

        # RIGHT
        with col3:
            st.markdown(
                f'<div class="date-text">{datetime.today().strftime("%d %b %Y")}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem !important;
        }

        .card {
            background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
            border: 1px solid rgba(122, 60, 255, 0.18);
            border-radius: 16px;
            padding: 18px 20px;
            margin-bottom: 10px;
        }

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
        }

        .date {
            color: white;
            font-size: 14px;
            font-weight: 700;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([5, 2, 2], vertical_alignment="center")

        with col1:
            st.markdown('<div class="title">Tally Ho TQ & RFI Tracker</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtitle">TQs • RFIs • Outstanding Responses</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="status"><span class="dot">●</span>Live System Status: Active</div>', unsafe_allow_html=True)

        with col3:
            st.markdown(
                f'<div class="date">{datetime.today().strftime("%d %b %Y")}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)
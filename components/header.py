import streamlit as st
from datetime import datetime

def render_header():

    st.markdown("""
    <style>
    /* Main header container */
    .header-wrapper {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
        min-height: 110px;
        margin-bottom: 10px;
    }

    /* Titles */
    .title {
        color: white;
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 4px;
        line-height: 1.1;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
    }

    /* Status pill */
    .status {
        display: inline-block;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);
        color: white;
        font-size: 13px;
        font-weight: 700;
        text-align: center;
        width: 100%;
    }

    .dot {
        color: #22c55e;
        font-weight: 900;
        margin-right: 6px;
    }

    /* Date + export */
    .date {
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-align: right;
    }

    .export {
        margin-top: 8px;
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 9px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        text-align: center;
    }

    /* Prevent shrinking issues */
    .block-container {
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ONE unified container (prevents broken layout gaps)
    with st.container():
        st.markdown('<div class="header-wrapper">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([5, 3, 2], gap="small")

        # LEFT
        with col1:
            st.markdown("""
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">TQs • RFIs • Outstanding Responses</div>
            """, unsafe_allow_html=True)

        # MIDDLE
        with col2:
            st.markdown("""
            <div class="status">
                <span class="dot">●</span> Live System Status: Active
            </div>
            """, unsafe_allow_html=True)

        # RIGHT
        with col3:
            st.markdown(f"""
            <div class="date">{datetime.today().strftime('%d %b %Y')}</div>
            <div class="export">⬇ Export Report</div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
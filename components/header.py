import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    /* REMOVE STREAMLIT TOP SPACING */
    .block-container {
        padding-top: 0rem !important;
    }

    /* MAIN HEADER CONTAINER */
    .header-box {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        flex-wrap: nowrap;

        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        border-radius: 16px;

        padding: 16px 22px;
        width: 100%;
        box-sizing: border-box;

        gap: 20px;
    }

    /* LEFT SECTION */
    .left {
        display: flex;
        flex-direction: column;
        min-width: 320px;
    }

    .title {
        color: white;
        font-size: 24px;
        font-weight: 900;
        line-height: 1.1;
        white-space: nowrap;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
        white-space: nowrap;
    }

    /* STATUS CENTER */
    .status-box {
        display: flex;
        align-items: center;
        gap: 8px;

        padding: 10px 14px;
        border-radius: 10px;

        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);

        color: white;
        font-size: 13px;
        font-weight: 700;

        white-space: nowrap;
        flex-shrink: 0;
    }

    .dot {
        color: #22c55e;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {opacity:1;}
        50% {opacity:0.4;}
        100% {opacity:1;}
    }

    /* RIGHT DATE */
    .date-text {
        color: white;
        font-size: 14px;
        font-weight: 700;

        white-space: nowrap;
        flex-shrink: 0;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header-box">

        <!-- LEFT -->
        <div class="left">
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">TQs • RFIs • Outstanding Responses</div>
        </div>

        <!-- CENTER -->
        <div class="status-box">
            <span class="dot">●</span>
            Live System Status: Active
        </div>

        <!-- RIGHT -->
        <div class="date-text">
            {datetime.today().strftime('%d %b %Y')}
        </div>

    </div>
    """, unsafe_allow_html=True)
import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        min-height: 95px;
        border-radius: 16px;
        padding: 18px 22px;

        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .left {
        display: flex;
        flex-direction: column;
    }

    .title {
        color: white;
        font-size: 26px;
        font-weight: 900;
        line-height: 1.1;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    .status-box {
        display: inline-flex;
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

    .date-text {
        color: white;
        font-size: 14px;
        font-weight: 700;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header-box">

        <!-- LEFT -->
        <div class="left">
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">
                TQs • RFIs • Outstanding Responses
            </div>
        </div>

        <!-- MIDDLE -->
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
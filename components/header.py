import streamlit as st
from datetime import datetime

def render_header():

    st.markdown("""
    <style>

    .header-wrapper {
        display: flex;
        width: 100%;
        gap: 0px;
        margin-bottom: 10px;
    }

    .card {
        flex: 1;
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        padding: 18px 20px;
        min-height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
    }

    .left {
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
    }

    .right {
        border-top-right-radius: 16px;
        border-bottom-right-radius: 16px;
    }

    .title {
        color: white;
        font-size: 26px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
    }

    .status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        color: white;
        font-size: 13px;
        font-weight: 700;
        padding: 10px 12px;
        border-radius: 10px;
        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);
        width: fit-content;
        margin: auto;
    }

    .dot {
        color: #22c55e;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {opacity: 1;}
        50% {opacity: 0.4;}
        100% {opacity: 1;}
    }

    .date {
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-align: right;
    }

    .btn {
        margin-top: 10px;
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        text-align: center;
        cursor: pointer;
    }

    </style>
    """, unsafe_allow_html=True)

    date_today = datetime.today().strftime('%d %b %Y')

    st.markdown(f"""
    <div class="header-wrapper">

        <!-- LEFT CARD -->
        <div class="card left">
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">TQs • RFIs • Outstanding Responses</div>
        </div>

        <!-- MIDDLE CARD -->
        <div class="card" style="align-items:center;">
            <div class="status">
                <span class="dot">●</span>
                Live System Status: Active
            </div>
        </div>

        <!-- RIGHT CARD -->
        <div class="card right">
            <div class="date">{date_today}</div>
            <div class="btn">⬇ Export Report</div>
        </div>

    </div>
    """, unsafe_allow_html=True)
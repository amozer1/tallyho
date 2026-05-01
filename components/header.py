import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    /* ===== FIXED STICKY HEADER WRAPPER ===== */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;

        background: linear-gradient(135deg, #0b1a2f 0%, #0f2440 100%);
        border-bottom: 1px solid rgba(122, 60, 255, 0.18);
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);

        padding: 12px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
    }

    /* Push page content below sticky header */
    .main .block-container {
        padding-top: 110px;
    }

    /* Title block */
    .title {
        color: white;
        font-size: 20px;
        font-weight: 800;
        line-height: 1.2;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
    }

    /* Status pill */
    .status {
        margin-left: auto;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: white;
        font-size: 12px;
        font-weight: 700;
    }

    .dot {
        color: #22c55e;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {opacity:1;}
        50% {opacity:0.3;}
        100% {opacity:1;}
    }

    .date {
        color: white;
        font-size: 13px;
        font-weight: 700;
        margin-left: 20px;
        white-space: nowrap;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sticky-header">

        <div>
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">TQs • RFIs • Outstanding Responses</div>
        </div>

        <div class="status">
            <span class="dot">●</span>
            Live System Active
        </div>

        <div class="date">
            {datetime.today().strftime('%d %b %Y')}
        </div>

    </div>
    """, unsafe_allow_html=True)
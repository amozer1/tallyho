import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    /* ===== STICKY WRAPPER (TARGET STREAMLIT CONTAINER) ===== */
    header[data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stAppViewContainer"] > div:first-child {
        padding-top: 0rem;
    }

    /* Custom sticky bar */
    .sticky-bar {
        position: sticky;
        top: 0;
        z-index: 999;

        background: linear-gradient(135deg, #0b1a2f 0%, #0f2440 100%);
        border-bottom: 1px solid rgba(122, 60, 255, 0.2);

        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 16px;

        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }

    /* Title */
    .title {
        color: white;
        font-size: 18px;
        font-weight: 800;
        line-height: 1.2;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
    }

    /* Status */
    .status {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
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
        0% {opacity: 1;}
        50% {opacity: 0.3;}
        100% {opacity: 1;}
    }

    .date {
        color: white;
        font-size: 13px;
        font-weight: 700;
        margin-left: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sticky-bar">

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
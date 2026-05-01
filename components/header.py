import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    /* =========================
       FIX STREAMLIT DEFAULT HEADER
    ========================= */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* =========================
       MAKE TOP APP CONTAINER STICKY
       (REAL STREAMLIT SAFE METHOD)
    ========================= */
    div[data-testid="stAppViewContainer"] > div:first-child {
        position: sticky;
        top: 0;
        z-index: 9999;
        background: #0b1a2f;
        padding-top: 6px;
        padding-bottom: 6px;
    }

    /* =========================
       HEADER BOX STYLE (UNCHANGED DESIGN)
    ========================= */
    .header-box {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.18);
        min-height: 95px;
        border-radius: 0px;
        padding: 18px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
    }

    .left-box {
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
    }

    .right-box {
        border-top-right-radius: 16px;
        border-bottom-right-radius: 16px;
    }

    /* =========================
       TEXT STYLES
    ========================= */
    .title {
        color: white;
        font-size: 26px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 12px;
    }

    .status-box {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);
        color: white;
        font-size: 13px;
        font-weight: 700;
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

    /* =========================
       CENTER DATE
    ========================= */
    .date-center {
        color: white;
        font-size: 15px;
        font-weight: 800;
        text-align: center;
        width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER LAYOUT
    # =========================
    col1, col2, col3 = st.columns([5, 3, 2], gap="small")

    with col1:
        st.markdown("""
        <div class="header-box left-box">
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">TQs • RFIs • Outstanding Responses</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="header-box" style="align-items:center; text-align:center;">
            <div class="date-center">
                {datetime.today().strftime('%d %b %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="header-box right-box" style="align-items:center;">
            <div class="status-box">
                <span class="dot">●</span>
                Live System Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)
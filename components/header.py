import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>
    /* Shared unified style */
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

    /* left rounded */
    .left-box {
        border-top-left-radius: 16px;
        border-bottom-left-radius: 16px;
    }

    /* right rounded */
    .right-box {
        border-top-right-radius: 16px;
        border-bottom-right-radius: 16px;
    }

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

    .date-text {
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-align:right;
    }

    .export-btn {
        margin-top: 8px;
        display:inline-block;
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 9px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        float:right;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([5, 3, 2], gap="small")

    with col1:
        st.markdown("""
        <div class="header-box left-box">
            <div class="title">Tally Ho TQ & RFI Tracker</div>
            <div class="subtitle">
                TQs • RFIs • Outstanding Responses
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="header-box" style="align-items:center; text-align:center;">
            <div class="status-box">
                <span class="dot">●</span>
                Live System Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="header-box right-box">
            <div class="date-text">{datetime.today().strftime('%d %b %Y')}</div>
            <div class="export-btn">⬇ Export Report</div>
        </div>
        """, unsafe_allow_html=True)
import streamlit as st
from datetime import datetime

def render_header():

    # ===== minimal styling ONLY (no layout control) =====
    st.markdown("""
    <style>

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
        font-size: 13px;
        font-weight: 700;
        color: white;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);
        display: inline-flex;
        gap: 8px;
        align-items: center;
        justify-content: center;
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
        font-size: 14px;
        font-weight: 700;
        color: white;
        text-align: right;
    }

    .btn {
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        text-align: center;
        margin-top: 8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ===== STREAMLIT LAYOUT ONLY =====
    col1, col2, col3 = st.columns([5, 3, 2], gap="small")

    # LEFT
    with col1:
        st.markdown('<div class="title">Tally Ho TQ & RFI Tracker</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">TQs • RFIs • Outstanding Responses</div>', unsafe_allow_html=True)

    # MIDDLE
    with col2:
        st.markdown("""
        <div style="text-align:center;">
            <div class="status">
                <span class="dot">●</span>
                Live System Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT
    with col3:
        st.markdown(f'<div class="date">{datetime.today().strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="btn">⬇ Export Report</div>', unsafe_allow_html=True)
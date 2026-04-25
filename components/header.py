import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    .header-container {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.25);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 0 18px rgba(122, 60, 255, 0.10);
    }

    .title {
        color: white;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #9fb3c8;
        font-size: 12px;
    }

    .status-box {
        display: inline-flex;
        align-items: center;
        gap: 6px;

        padding: 8px 12px;
        border-radius: 10px;

        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);

        color: #cbd5e1;
        font-size: 13px;
        font-weight: 600;
    }

    .dot {
        color: #22c55e;
        animation: pulse 1.6s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }

    .export-btn {
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        text-align: center;
    }

    .date-text {
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-align: right;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # STREAMLIT LAYOUT (STABLE)
    # =========================
    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        st.markdown("""
        <div class="header-container">
            <div class="title">TQ / RFI Intelligence Hub</div>
            <div class="subtitle">
                Project Controls • SLA Monitoring • Response Analytics
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="header-container" style="text-align:center;">
            <div class="status-box">
                <span class="dot">●</span>
                Live System Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="header-container" style="text-align:right;">
            <div class="date-text">{datetime.today().strftime('%d %b %Y')}</div>
            <div style="margin-top:8px;" class="export-btn">⬇ Export Report</div>
        </div>
        """, unsafe_allow_html=True)
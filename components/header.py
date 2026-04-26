import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("""
    <style>

    /* MAIN WRAPPER */
    .main-header {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.20);
        border-radius: 18px;
        padding: 14px 22px;
        box-shadow: 0 0 20px rgba(122, 60, 255, 0.10);
        margin-bottom: 12px;
    }

    /* LEFT */
    .title {
        color: white;
        font-size: 28px;
        font-weight: 900;
        line-height: 1.1;
        margin: 0;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
        letter-spacing: 0.3px;
    }

    /* MIDDLE STATUS */
    .status-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .status-box {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        border-radius: 12px;
        background: rgba(122, 60, 255, 0.10);
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
        0% {opacity: 1;}
        50% {opacity: 0.4;}
        100% {opacity: 1;}
    }

    /* RIGHT */
    .right-wrap {
        text-align: right;
    }

    .date-text {
        color: white;
        font-size: 14px;
        font-weight: 700;
    }

    .export-btn {
        margin-top: 8px;
        display: inline-block;
        background: linear-gradient(135deg, #7a3cff, #8b5cf6);
        color: white;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        box-shadow: 0 4px 14px rgba(122, 60, 255, 0.25);
    }

    </style>
    """, unsafe_allow_html=True)

    # unified header background
    st.markdown('<div class="main-header">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([5, 3, 2])

    with col1:
        st.markdown("""
            <div class="title">TQ / RFI Intelligence Hub</div>
            <div class="subtitle">
                Project Controls • SLA Monitoring • Response Analytics
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="status-wrap">
                <div class="status-box">
                    <span class="dot">●</span>
                    Live System Status: Active
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="right-wrap">
                <div class="date-text">{datetime.today().strftime('%d %b %Y')}</div>
                <div class="export-btn">⬇ Export Report</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
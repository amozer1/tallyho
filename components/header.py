import streamlit as st
from datetime import datetime


def render_header():
    st.markdown("""
    <style>

    .header-bar {
        background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
        border: 1px solid rgba(122, 60, 255, 0.25);
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);

        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
    }

    .brand {
        display: flex;
        flex-direction: column;
    }

    .title {
        color: white;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 0.4px;
    }

    .subtitle {
        color: #9fb3c8;
        font-size: 12px;
        margin-top: 4px;
    }

    .status {
        color: #cbd5e1;
        font-size: 13px;
        font-weight: 600;
        text-align: center;
        padding: 8px 14px;
        border-radius: 10px;
        background: rgba(122, 60, 255, 0.12);
        border: 1px solid rgba(122, 60, 255, 0.25);
    }

    .status-dot {
        color: #22c55e;
        margin-right: 6px;
    }

    .right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
    }

    .date {
        color: white;
        font-size: 14px;
        font-weight: 700;
    }

    .export {
        background: linear-gradient(135deg, #7a3cff 0%, #8b5cf6 100%);
        color: white;
        font-size: 13px;
        font-weight: 800;
        padding: 10px 14px;
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(122, 60, 255, 0.35);
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header-bar">

        <!-- LEFT -->
        <div class="brand">
            <div class="title">TQ / RFI Intelligence Hub</div>
            <div class="subtitle">Project Controls • SLA Monitoring • Response Analytics</div>
        </div>

        <!-- CENTER -->
        <div class="status">
            <span class="status-dot">●</span>
            Live System Status: Active
        </div>

        <!-- RIGHT -->
        <div class="right">
            <div class="date">{datetime.today().strftime('%d %b %Y')}</div>
            <div class="export">⬇ Export Report</div>
        </div>

    </div>
    """, unsafe_allow_html=True)
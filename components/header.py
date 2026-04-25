import streamlit as st
from datetime import datetime


def render_header():
    st.markdown("""
    <style>
        .header-card {
            background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
            border: 1px solid rgba(0,191,255,0.25);
            border-radius: 16px;
            padding: 18px 22px;
            box-shadow: 0 0 18px rgba(0,191,255,0.08);
            min-height: 95px;
        }

        .header-title {
            color: white;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.4px;
        }

        .header-subtitle {
            color: #9fb3c8;
            font-size: 13px;
            margin-top: 4px;
        }

        .date-title {
            color: white;
            font-size: 16px;
            font-weight: 700;
        }

        .date-sub {
            color: #9fb3c8;
            font-size: 11px;
            margin-top: 4px;
        }

        .download-btn {
            background: linear-gradient(135deg, #00bfff 0%, #00ffd5 100%);
            color: black;
            font-size: 14px;
            font-weight: 700;
            padding: 12px;
            border-radius: 12px;
            text-align:center;
            box-shadow: 0 0 15px rgba(0,255,213,0.35);
        }

        .download-sub {
            color:#9fb3c8;
            font-size:11px;
            margin-top:5px;
            text-align:center;
        }
    </style>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([4, 2, 1.5])

    with left:
        st.markdown("""
        <div class="header-card">
            <div class="header-title">
                TQ and RFI Dashboard
            </div>
            <div class="header-subtitle">
                Project Overview and Service Level Agreement Performance
            </div>
        </div>
        """, unsafe_allow_html=True)

    with middle:
        st.markdown(f"""
        <div class="header-card" style="text-align:center;">
            <div class="date-title">
                {datetime.today().strftime('%d %b %Y')}
            </div>
            <div class="date-sub">
                Last Updated
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="header-card">
            <div class="download-btn">
                ⬇ Export Report
            </div>
            <div class="download-sub">
                Download latest analytics
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
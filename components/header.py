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

        .title {
            color: white;
            font-size: 26px;
            font-weight: 900;
            letter-spacing: 0.4px;
        }

        .subtitle {
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

        .download {
            background: linear-gradient(135deg, #00bfff 0%, #00ffd5 100%);
            color: black;
            font-size: 14px;
            font-weight: 800;
            padding: 12px;
            border-radius: 12px;
            text-align:center;
            box-shadow: 0 0 15px rgba(0,255,213,0.35);
        }

        .rainbow-line {
            height: 3px;
            width: 100%;
            margin-top: 12px;
            border-radius: 5px;
            background: linear-gradient(
                90deg,
                #ff0000,
                #ff7f00,
                #ffff00,
                #00ff00,
                #00ffff,
                #0000ff,
                #8b00ff
            );
            box-shadow: 0 0 10px rgba(0,191,255,0.25);
        }
    </style>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([4, 2, 1.5])

    # =========================
    # LEFT TITLE
    # =========================
    with left:
        st.markdown("""
        <div class="header-card">
            <div class="title">
                TQ & RFI Performance Control Centre
            </div>
            <div class="subtitle">
                Project Overview and Service Level Agreement Performance
            </div>
        </div>

        <div class="rainbow-line"></div>
        """, unsafe_allow_html=True)

    # =========================
    # DATE
    # =========================
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

        <div class="rainbow-line"></div>
        """, unsafe_allow_html=True)

    # =========================
    # DOWNLOAD
    # =========================
    with right:
        st.markdown("""
        <div class="header-card">
            <div class="download">
                ⬇ Export Report
            </div>
            <div style="
                color:#9fb3c8;
                font-size:11px;
                margin-top:5px;
                text-align:center;
            ">
                Download latest analytics
            </div>
        </div>

        <div class="rainbow-line"></div>
        """, unsafe_allow_html=True)
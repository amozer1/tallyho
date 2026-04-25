import streamlit as st
from datetime import datetime


def render_header():
    st.markdown("""
    <style>
        .header-wrapper {
            background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
            border: 1px solid rgba(122, 60, 255, 0.25);
            border-radius: 16px;
            padding: 18px 22px 10px 22px;
            box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
        }

        .header-card {
            background: transparent;
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
            text-align: center;
        }

        .date-sub {
            color: #9fb3c8;
            font-size: 11px;
            text-align: center;
            margin-top: 4px;
        }

        .download {
            background: linear-gradient(135deg, #7a3cff 0%, #8b5cf6 100%);
            color: white;
            font-size: 14px;
            font-weight: 800;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 0 15px rgba(122, 60, 255, 0.35);
        }

        /* 🔥 FULL-WIDTH UNBROKEN LINE */
        .purple-line {
            height: 4px;
            width: 100%;
            margin-top: 14px;
            border-radius: 6px;
            background: linear-gradient(
                90deg,
                #6a00ff,
                #8b5cf6,
                #6a00ff
            );
            box-shadow: 0 0 12px rgba(138, 43, 226, 0.35);
        }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # WRAPPER (IMPORTANT FIX)
    # =========================
    st.markdown('<div class="header-wrapper">', unsafe_allow_html=True)

    left, middle, right = st.columns([4, 2, 1.5])

    # LEFT
    with left:
        st.markdown("""
        <div class="header-card">
            <div class="title">TQ / RFI Intelligence Hub</div>
            <div class="subtitle">Project Controls • SLA Monitoring • Response Analytics</div>
        </div>
        """, unsafe_allow_html=True)

    # MIDDLE
    with middle:
        st.markdown(f"""
        <div class="header-card">
            <div class="date-title">{datetime.today().strftime('%d %b %Y')}</div>
            <div class="date-sub">Last Updated</div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT
    with right:
        st.markdown("""
        <div class="header-card">
            <div class="download">⬇ Export Report</div>
            <div style="
                color:#9fb3c8;
                font-size:11px;
                margin-top:5px;
                text-align:center;
            ">
                Download latest analytics
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # FULL WIDTH LINE (FIXED)
    # =========================
    st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
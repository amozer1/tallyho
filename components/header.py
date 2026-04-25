import streamlit as st
from datetime import datetime


def render_header():
    st.markdown("""
    <style>
        .header-card {
            background: linear-gradient(135deg, #0b1a2f 0%, #102845 100%);
            border: 1px solid rgba(122, 60, 255, 0.25);
            border-radius: 16px;
            padding: 18px 22px;
            box-shadow: 0 0 18px rgba(122, 60, 255, 0.08);
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
            background: linear-gradient(135deg, #7a3cff 0%, #8b5cf6 100%);
            color: white;
            font-size: 14px;
            font-weight: 800;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 0 15px rgba(122, 60, 255, 0.35);
        }

        /* 🔥 PREMIUM PURPLE SEPARATOR LINE */
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
            opacity: 0.95;
        }
    </style>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([4, 2, 1.5])

    # =========================
    # LEFT - TITLE
    # =========================
    with left:
        st.markdown("""
        <div class="header-card">
            <div class="title">
                TQ / RFI Intelligence Hub
            </div>
            <div class="subtitle">
                Project Controls • SLA Monitoring • Response Analytics
            </div>
        </div>

        <div class="purple-line"></div>
        """, unsafe_allow_html=True)

    # =========================
    # MIDDLE - DATE
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

        <div class="purple-line"></div>
        """, unsafe_allow_html=True)

    # =========================
    # RIGHT - EXPORT
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

        <div class="purple-line"></div>
        """, unsafe_allow_html=True)
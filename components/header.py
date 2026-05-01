import streamlit as st
from datetime import datetime


def render_header():
    # Remove top padding so header sits tight
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout
    col1, col2, col3 = st.columns([5, 2, 2], vertical_alignment="center")

    # ================= LEFT =================
    with col1:
        st.markdown(
            """
            <div style="display:flex; flex-direction:column;">
                <div style="
                    color:white;
                    font-size:24px;
                    font-weight:900;
                    line-height:1.1;">
                    Tally Ho TQ & RFI Tracker
                </div>

                <div style="
                    color:#94a3b8;
                    font-size:12px;
                    margin-top:4px;">
                    TQs • RFIs • Outstanding Responses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= CENTER =================
    with col2:
        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                gap:8px;

                padding:10px 14px;
                border-radius:10px;

                background:rgba(122,60,255,0.12);
                border:1px solid rgba(122,60,255,0.25);

                color:white;
                font-size:13px;
                font-weight:700;
                white-space:nowrap;">

                <span style="color:#22c55e;">●</span>
                Live System Status: Active
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= RIGHT =================
    with col3:
        st.markdown(
            f"""
            <div style="
                color:white;
                font-size:14px;
                font-weight:700;
                text-align:right;
                white-space:nowrap;">

                {datetime.today().strftime('%d %b %Y')}
            </div>
            """,
            unsafe_allow_html=True
        )
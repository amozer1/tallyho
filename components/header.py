import streamlit as st
from datetime import datetime


def render_header():
    st.markdown("---")

    left, middle, right = st.columns([4, 2, 1.5])

    with left:
        st.markdown("""
        <div style="
            background:#0b1a2f;
            padding:16px;
            border-radius:12px;
            border:1px solid rgba(0,191,255,0.25);
            min-height:85px;
        ">
            <div style="
                color:white;
                font-size:22px;
                font-weight:800;
            ">
                TQ and RFI Dashboard
            </div>
            <div style="
                color:#9fb3c8;
                font-size:13px;
                margin-top:4px;
            ">
                Project Overview and Service Level Agreement Performance
            </div>
        </div>
        """, unsafe_allow_html=True)

    with middle:
        st.markdown(f"""
        <div style="
            background:#0b1a2f;
            padding:16px;
            border-radius:12px;
            border:1px solid rgba(0,191,255,0.25);
            text-align:center;
            min-height:85px;
        ">
            <div style="
                color:white;
                font-size:15px;
                font-weight:700;
            ">
                {datetime.today().strftime('%d %b %Y')}
            </div>
            <div style="
                color:#9fb3c8;
                font-size:11px;
                margin-top:4px;
            ">
                Last Updated
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div style="
            background:#0b1a2f;
            padding:16px;
            border-radius:12px;
            border:1px solid rgba(0,191,255,0.25);
            text-align:center;
            min-height:85px;
        ">
            <div style="
                color:#00bfff;
                font-size:13px;
                font-weight:700;
            ">
                Download Report
            </div>
            <div style="
                color:#9fb3c8;
                font-size:11px;
                margin-top:4px;
            ">
                Export Available
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
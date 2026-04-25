import streamlit as st
from datetime import datetime

st.markdown("---")

# =========================
# HEADER CONTAINER (STREAMLIT CONTROLLED LAYOUT)
# =========================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #0b1a2f, #0f2747);
        padding: 18px 22px;
        border-radius: 14px;
        border: 1px solid rgba(0,191,255,0.35);
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    ">
        <div style="color:white;font-size:22px;font-weight:800;">
            TQ and RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;margin-top:4px;">
            Project Overview and Service Level Agreement Performance
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #0b1a2f, #0f2747);
        padding: 18px 22px;
        border-radius: 14px;
        border: 1px solid rgba(0,191,255,0.35);
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
        text-align:right;
    ">
        <div style="color:white;font-size:15px;font-weight:600;">
            {datetime.today().strftime('%d %b %Y')}
        </div>
        <div style="color:#9fb3c8;font-size:12px;margin-top:4px;">
            Last Updated
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
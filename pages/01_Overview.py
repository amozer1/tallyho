import streamlit as st
from datetime import datetime

st.markdown("---")

# =========================
# HEADER ROW (CLEAN EXECUTIVE STYLE)
# =========================
left, middle, right = st.columns([4, 2, 1.2])

with left:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        height:100%;
    ">
        <div style="color:white;font-size:22px;font-weight:800;">
            TQ and RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;margin-top:4px;">
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
        height:100%;
    ">
        <div style="color:white;font-size:15px;font-weight:700;">
            {datetime.today().strftime('%d %b %Y')}
        </div>
        <div style="color:#9fb3c8;font-size:11px;margin-top:4px;">
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
        height:100%;
    ">
        <div style="color:#00bfff;font-size:13px;font-weight:700;">
            Download
        </div>
        <div style="color:#9fb3c8;font-size:11px;margin-top:4px;">
            Report Export
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
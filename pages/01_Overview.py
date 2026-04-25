import streamlit as st
from datetime import datetime

st.markdown("---")

# =========================
# HEADER (STREAMLIT SAFE)
# =========================
left, mid, right = st.columns([3, 1.5, 1])

with left:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:14px 16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
    ">
        <div style="color:white;font-size:22px;font-weight:800;">
            TQ and RFI Dashboard
        </div>
        <div style="color:#9fb3c8;font-size:13px;margin-top:4px;">
            Project Overview and Service Level Agreement Performance
        </div>
    </div>
    """, unsafe_allow_html=True)

with mid:
    st.markdown(f"""
    <div style="
        background:#0b1a2f;
        padding:14px 16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        text-align:center;
    ">
        <div style="color:white;font-size:15px;font-weight:700;">
            {datetime.today().strftime('%d %b %Y')}
        </div>
        <div style="color:#9fb3c8;font-size:11px;">
            Last Updated
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="
        background:#0b1a2f;
        padding:14px 16px;
        border-radius:12px;
        border:1px solid rgba(0,191,255,0.25);
        text-align:right;
    ">
        <div style="color:#00bfff;font-size:12px;font-weight:600;">
            Download
        </div>
        <div style="color:#9fb3c8;font-size:11px;">
            Report export available below
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
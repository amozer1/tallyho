import streamlit as st
from datetime import datetime


def render_header():

    # Optional: reduce top spacing
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout (this is your "continuous header")
    col1, col2, col3 = st.columns([5, 2, 2], vertical_alignment="center")

    # ================= LEFT =================
    with col1:
        st.subheader("Tally Ho TQ & RFI Tracker")
        st.caption("TQs • RFIs • Outstanding Responses")

    # ================= CENTER =================
    with col2:
        st.success("● Live System Status: Active")

    # ================= RIGHT =================
    with col3:
        st.markdown(
            f"**{datetime.today().strftime('%d %b %Y')}**",
            help="Current system date"
        )
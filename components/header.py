import streamlit as st
from datetime import datetime


def render_header():

    # Page spacing control
    st.markdown("")

    # =========================
    # HEADER ROW (3 COLUMNS)
    # =========================
    col1, col2, col3 = st.columns([5, 3, 2], gap="small")

    # =========================
    # LEFT: TITLE BLOCK
    # =========================
    with col1:
        st.markdown("## 🏗️ Tally Ho TQ & RFI Tracker")
        st.caption("TQs • RFIs • Outstanding Responses")

    # =========================
    # MIDDLE: STATUS BLOCK
    # =========================
    with col2:
        st.success("● Live System Status: Active")

    # =========================
    # RIGHT: DATE + EXPORT
    # =========================
    with col3:
        st.markdown(f"**📅 {datetime.today().strftime('%d %b %Y')}**")
        st.button("⬇ Export Report")

    # =========================
    # DIVIDER (CARD FEEL)
    # =========================
    st.divider()
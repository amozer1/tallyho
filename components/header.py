import streamlit as st
from datetime import datetime


def render_header():

    st.markdown("")

    # =========================
    # SINGLE HEADER ROW
    # =========================
    with st.container():

        col1, col2, col3 = st.columns([6, 3, 2], gap="small")

        # LEFT: TITLE
        with col1:
            st.markdown("### 🏗️ Tally Ho TQ & RFI Tracker")
            st.caption("TQs • RFIs • Outstanding Responses")

        # MIDDLE: STATUS
        with col2:
            st.success("● Live System Status: Active")

        # RIGHT: DATE + ACTION
        with col3:
            st.markdown(f"**📅 {datetime.today().strftime('%d %b %Y')}**")
            st.button("⬇ Export Report", use_container_width=True)

    # subtle separator to keep dashboard structure clean
    st.divider()
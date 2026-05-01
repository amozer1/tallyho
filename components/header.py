import streamlit as st
from datetime import datetime


def render_header():

    # spacing control
    st.markdown("")

    # =========================
    # MAIN HEADER CARD CONTAINER
    # =========================
    with st.container():

        # top row = title + status + date/export
        col1, col2, col3 = st.columns([6, 3, 2], gap="small")

        # ================= LEFT =================
        with col1:
            st.markdown("### 🏗️ Tally Ho TQ & RFI Tracker")
            st.caption("TQs • RFIs • Outstanding Responses")

        # ================= MIDDLE =================
        with col2:
            st.metric(
                label="System Status",
                value="Active",
                delta="Live"
            )

        # ================= RIGHT =================
        with col3:
            st.markdown(f"**📅 {datetime.today().strftime('%d %b %Y')}**")
            st.button("⬇ Export Report", use_container_width=True)

    # =========================
    # KPI STRIP (makes it look like a dashboard)
    # =========================
    st.markdown("---")

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric("Open", "15", "⬆ 2")

    with k2:
        st.metric("Outstanding", "13", "⬆ 1")

    with k3:
        st.metric("Closed", "1", "⬇ 3")

    st.markdown("---")
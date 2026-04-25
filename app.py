import streamlit as st

from components.sidebar import render_sidebar
from components.header import render_header


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)


# =========================
# GLOBAL UI COMPONENTS
# =========================
render_sidebar()
render_header()


# =========================
# ROUTING NOTE
# =========================
st.markdown("""
## Select a page from the sidebar to begin analysis.
""")
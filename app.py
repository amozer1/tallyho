import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.tracker import render_tracker  # ✅ UPDATED IMPORT
from components.overdue_alert import render_overdue_alert, render_overdue_button


st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

# =========================
# UI FRAMEWORK
# =========================
render_sidebar()
render_header()

# =========================
# DATA LOADING (GITHUB SAFE)
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")  # must exist in repo

df = load_data()

# =========================
# TRACKER MODULE (STAGE 3 ANALYTICS)
# =========================
render_tracker(df)
import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.header import render_header
from components.tracker import render_tracker
from components.outstanding import render_outstanding_line
from components.age_outstanding import render_age_outstanding
from components.trend import render_trend

st.set_page_config(
    page_title="TQ / RFI Intelligence Hub",
    layout="wide"
)

render_sidebar()
render_header()

@st.cache_data
def load_data():
    return pd.read_excel("data/TQ_TH.xlsx")

df = load_data()

df = df.copy()
df.columns = df.columns.str.strip().str.lower()

df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

today = pd.Timestamp.today().normalize()
df["age"] = (today - df["date sent"]).dt.days

st.markdown("## 📊 TQ / RFI Control Dashboard")

# ROW 1
col1, col2 = st.columns(2)

with col1:
    with st.container():
        render_trend(df)

with col2:
    with st.container():
        render_outstanding_line(df, total=len(df))

# ROW 2
col3, col4 = st.columns(2)

with col3:
    with st.container():
        render_age_outstanding(df)

with col4:
    with st.container():
        render_tracker(df)
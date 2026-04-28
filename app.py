import streamlit as st

# import your modules
from components.age_outstanding import render_age_outstanding
from components.outstanding import render_outstanding
from components.trend import render_trend


def render_dashboard(df):

    st.set_page_config(layout="wide")

    # =========================
    # 3 EQUAL PANELS
    # =========================
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("### Age Outstanding")
        render_age_outstanding(df)

    with col2:
        st.markdown("### Outstanding")
        render_outstanding(df)

    with col3:
        st.markdown("### Trend Analysis")
        render_trend(df)
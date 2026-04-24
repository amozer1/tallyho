import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="TQ & RFI AI Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")
    return df

df = load_data()

# ---------- SIDEBAR ----------
st.sidebar.image("assets/logo.png", width=100)
st.sidebar.title("Navigation")

menu = [
    "Overview",
    "TQs",
    "RFIs",
    "Analytics",
    "AI Insights",
    "Predictive Risk",
    "Response Performance",
    "Reports",
    "Settings"
]

choice = st.sidebar.radio("", menu)

# ---------- CSS ----------
st.markdown("""
<style>
.big-font {
    font-size:28px !important;
    font-weight:bold;
}
.metric-box{
    background:#111827;
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 10px rgba(0,0,0,.4);
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
col1, col2 = st.columns([6,2])
with col1:
    st.markdown('<p class="big-font">TQ & RFI AI Dashboard</p>', unsafe_allow_html=True)
    st.caption("Project Overview & Response Analytics")
with col2:
    st.date_input("")

# ---------- KPI ----------
k1,k2,k3,k4 = st.columns(4)

with k1:
    st.metric("Total TQs", len(df))
with k2:
    st.metric("Total RFIs", len(df[df["Type"]=="RFI"]))
with k3:
    st.metric("Closed (30 Days)", len(df[df["Status"]=="Closed"]))
with k4:
    overdue = len(df[df["Days Open"] > 7])
    st.metric("Overdue (>7 Days)", overdue)

# ---------- VENN STYLE ----------
st.subheader("Not Responded within 7 Days")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.4)", line_color="rgba(0,102,255,1)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(102,0,255,0.4)", line_color="rgba(102,0,255,1)")
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
              fillcolor="rgba(0,255,102,0.4)", line_color="rgba(0,255,102,1)")

fig.add_annotation(x=1, y=1, text="TQ Only<br>24%")
fig.add_annotation(x=2, y=1, text="Both<br>12%")
fig.add_annotation(x=3, y=1, text="RFI Only<br>18%")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(
    height=400,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#0B1220"
)

st.plotly_chart(fig, use_container_width=True)

# ---------- CHARTS ----------
c1,c2,c3 = st.columns(3)

with c1:
    st.subheader("TQ & RFI Trend")
    trend = px.line(df, x="Date", y="Days Open", color="Type")
    st.plotly_chart(trend, use_container_width=True)

with c2:
    st.subheader("Outstanding by Age")
    age_bins = pd.cut(df["Days Open"], bins=[0,2,7,14,30,100])
    age_count = age_bins.value_counts()
    age_fig = px.bar(age_count)
    st.plotly_chart(age_fig, use_container_width=True)

with c3:
    st.subheader("AI Risk Prediction")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=72,
        title={'text': "High Risk"},
        gauge={'axis': {'range': [0,100]}}
    ))
    gauge.update_layout(paper_bgcolor="#0B1220")
    st.plotly_chart(gauge, use_container_width=True)

# ---------- AI INSIGHTS ----------
st.subheader("AI Insights & Recommendations")

a1,a2,a3 = st.columns(3)
with a1:
    st.info("28 items are at high risk of delay.")
with a2:
    st.success("Mechanical has the highest overdue items.")
with a3:
    st.warning("Consider auto-reminders for overdue items.")
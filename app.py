import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

from utils.data_loader import load_data
from utils.metrics import get_metrics
from utils.ml_model import train_model, load_model, predict_risk

# =========================
# AUTO REFRESH (LIVE DASHBOARD)
# =========================
st_autorefresh(interval=30000, key="refresh")  # every 30 sec

# =========================
# LOAD DATA
# =========================
df = load_data()
m = get_metrics(df)

# =========================
# TRAIN / LOAD MODEL (AUTO)
# =========================
if not df.empty:
    try:
        model = load_model()
    except:
        model = train_model(df)
else:
    model = None

if model and not df.empty:
    df = predict_risk(model, df)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide", page_title="TQ & RFI ML Dashboard")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([3,1])

with col1:
    st.title("📊 TQ & RFI ML Dashboard")
    st.caption("Live Engineering Intelligence System")

with col2:
    st.metric("Last Refresh", datetime.now().strftime("%H:%M:%S"))

# =========================
# KPI ROW
# =========================
k1,k2,k3,k4 = st.columns(4)

k1.metric("TQ", m["total_tq"])
k2.metric("RFI", m["total_rfi"])
k3.metric("Closed", m["closed"])
k4.metric("Overdue 7+ Days", m["overdue7"])

# =========================
# MAIN GRID
# =========================
left, right = st.columns([2,1])

# ---------------- LEFT ----------------
with left:

    st.subheader("📈 Trend Analysis")

    if not df.empty:
        trend = df.groupby(["Type"]).size().reset_index(name="Count")
        fig = px.bar(trend, x="Type", y="Count", color="Type")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Aging Distribution")

    if not df.empty:
        fig2 = px.histogram(df, x="AgeDays", color="Type")
        st.plotly_chart(fig2, use_container_width=True)

# ---------------- RIGHT (AI ENGINE) ----------------
with right:

    st.subheader("🧠 AI Risk Engine")

    if not df.empty and "RiskScore" in df.columns:

        avg_risk = df["RiskScore"].mean()

        st.metric("Average Risk", f"{avg_risk:.2f}")

        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_risk*100,
            gauge={
                "axis":{"range":[0,100]},
                "steps":[
                    {"range":[0,40],"color":"green"},
                    {"range":[40,70],"color":"orange"},
                    {"range":[70,100],"color":"red"}
                ]
            }
        ))

        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("⚠ High Risk Items")

    if not df.empty and "RiskScore" in df.columns:
        high_risk = df[df["RiskScore"] > 0.7]
        st.dataframe(high_risk[["Type","AgeDays","RiskScore"]])
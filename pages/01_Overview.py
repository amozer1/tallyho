import streamlit as st
from utils.data_loader import load_data
from utils.metrics import compute_metrics
import plotly.express as px
import plotly.graph_objects as go

df = load_data()
m = compute_metrics(df)

st.title("Overview Dashboard")

# KPI
c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
c1.metric("Total TQs", m["tq"])
c2.metric("Total RFIs", m["rfi"])
c3.metric("Closed", m["closed"])
c4.metric("Open", m["open"])
c5.metric("Overdue", m["overdue"])
c6.metric("Avg Resp", m["avg_response"])
c7.metric("SLA %", m["sla"])

# Trend
trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)
fig = px.line(trend)
st.plotly_chart(fig, use_container_width=True)

# Risk Gauge
risk_score = min(100, (m["overdue"]/m["total"])*100)
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk_score,
    title={"text":"AI Risk"},
    gauge={
        "axis":{"range":[0,100]},
        "steps":[
            {"range":[0,40],"color":"green"},
            {"range":[40,70],"color":"yellow"},
            {"range":[70,100],"color":"red"}
        ]
    }
))
st.plotly_chart(gauge, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(layout="wide")

df = load_data()
m = get_metrics(df)

st.markdown("# TQ & RFI ML Dashboard")
st.caption("Project overview and Response analytics")

# KPI Cards
c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric("Total TQs", m["total_tq"])
c2.metric("Total RFIs", m["total_rfi"])
c3.metric("Closed", m["closed"])
c4.metric("Open", m["open"])
c5.metric("Overdue >7", m["overdue7"])
c6.metric("SLA %", f"{m['sla']}%")

# Row 2
left, right = st.columns([2,1])

with left:
    st.subheader("TQ & RFI Trend")

    if not df.empty:
        trend = df.groupby(["DateSent","Type"]).size().reset_index(name="Count")
        fig = px.line(
            trend,
            x="DateSent",
            y="Count",
            color="Type",
            markers=True,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Outstanding by Age")

    if not df.empty:
        bins = [0,2,7,14,30,999]
        labels = ["0-2","3-7","8-14","15-30","30+"]
        df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

        age = df.groupby("AgeBand").size().reset_index(name="Count")
        fig2 = px.bar(
            age,
            x="Count",
            y="AgeBand",
            orientation="h",
            template="plotly_dark",
            color="Count"
        )
        st.plotly_chart(fig2, use_container_width=True)

# Risk Gauge
st.subheader("AI Risk Prediction")

risk = min(100, int((m["overdue7"]/max(1,m["open"]))*100))

fig3 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk,
    title={"text":"Risk"},
    gauge={
        "axis":{"range":[0,100]},
        "bar":{"color":"red"},
        "steps":[
            {"range":[0,40],"color":"green"},
            {"range":[40,70],"color":"orange"},
            {"range":[70,100],"color":"red"}
        ]
    }
))
fig3.update_layout(template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# AI Insights
st.subheader("AI Insights")

st.warning(f"{m['overdue7']} items overdue >7 days")
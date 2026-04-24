import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.metrics import compute_metrics

st.set_page_config(layout="wide")

file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(file) if file else load_data("data/TQ_TH.xlsx")

m = compute_metrics(df)

# KPI ROW
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("TQs", m["tq"])
c2.metric("RFIs", m["rfi"])
c3.metric("Open", m["open"])
c4.metric("Overdue >7", m["overdue7"])
c5.metric("SLA %", m["sla"])

st.markdown("---")

left, right = st.columns([2,1])

with left:

    st.subheader("TQ vs RFI")

    fig = px.pie(names=["TQ","RFI"], values=[m["tq"], m["rfi"]], hole=0.6)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Trend")

    trend = m["df"].groupby(m["df"]["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig2 = go.Figure()

    if "TQ" in trend:
        fig2.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))
    if "RFI" in trend:
        fig2.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

    st.plotly_chart(fig2, use_container_width=True)

with right:

    st.subheader("Ageing")

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]

    m["df"]["AgeBand"] = pd.cut(m["df"]["AgeDays"], bins=bins, labels=labels)

    st.bar_chart(m["df"]["AgeBand"].value_counts().reindex(labels).fillna(0))
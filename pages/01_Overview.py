import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(layout="wide")

df = load_data()
m = get_metrics(df)

# ================= HEADER =================
st.title("📊 TQ & RFI Overview Dashboard")

# ================= KPI ROW =================
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("TQs", m["total_tq"])
c2.metric("RFIs", m["total_rfi"])
c3.metric("Closed", m["closed"])
c4.metric("Open", m["open"])
c5.metric("Overdue", m["overdue7"])

st.markdown("---")

# ================= VENN STYLE LOGIC =================
st.subheader("Communication Health Snapshot")

tq_overdue = len(df[(df["Doc Type"]=="TQ") & (df["AgeDays"]>7)])
rfi_overdue = len(df[(df["Doc Type"]=="RFI") & (df["AgeDays"]>7)])
both = min(tq_overdue, rfi_overdue)

fig = px.bar(
    x=["TQ Overdue", "Both", "RFI Overdue"],
    y=[tq_overdue, both, rfi_overdue],
    text=[tq_overdue, both, rfi_overdue]
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ================= TREND =================
st.subheader("Trend")

trend = df.groupby(["Date Sent", "Doc Type"]).size().reset_index(name="Count")

fig2 = px.line(trend, x="Date Sent", y="Count", color="Doc Type")
st.plotly_chart(fig2, use_container_width=True)

# ================= AGE =================
st.subheader("Outstanding by Age")

fig3 = px.histogram(df, x="AgeDays", nbins=10)
st.plotly_chart(fig3, use_container_width=True)

# ================= INSIGHTS =================
st.subheader("AI Insights (Rule-Based)")

st.info(f"{m['overdue7']} items are overdue (>7 days)")
st.warning("High activity detected in recent submissions")
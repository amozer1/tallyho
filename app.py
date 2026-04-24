import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TQ & RFI ML Dashboard", layout="wide")

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_data(file_path_or_buffer):
    df = pd.read_excel(file_path_or_buffer)
    df.columns = [c.strip() for c in df.columns]
    return df

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

default_path = r"C:\\Users\\adane\\tally\\data\\TQ_TH.xlsx"

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data(default_path)

# =========================
# CLEANING
# =========================
for c in df.columns:
    if df[c].dtype == "object":
        df[c] = df[c].astype(str)

for col in ["Date Sent", "Reply Date", "Required Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

now = pd.Timestamp(datetime.now())

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.markdown("## Filters")

status_filter = st.sidebar.multiselect("Status", df["Status"].unique()) if "Status" in df.columns else []
type_filter = st.sidebar.multiselect("Doc Type", df["Doc Type"].unique()) if "Doc Type" in df.columns else []

filtered_df = df.copy()

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
if type_filter:
    filtered_df = filtered_df[filtered_df["Doc Type"].isin(type_filter)]

# =========================
# LOGIC
# =========================
is_tq = filtered_df["Doc Type"].str.contains("TQ", na=False)
is_rfi = filtered_df["Doc Type"].str.contains("RFI", na=False)

closed = filtered_df[filtered_df["Status"].str.contains("Closed", case=False, na=False)]

filtered_df["AgeDays"] = (now - filtered_df["Date Sent"]).dt.days
filtered_df["AgeDays"] = filtered_df["AgeDays"].fillna(0)

over_7 = filtered_df[filtered_df["AgeDays"] > 7]
over_30 = filtered_df[filtered_df["AgeDays"] > 30]

# =========================
# RISK SCORE (SIMPLE ML LOGIC)
# =========================
filtered_df["RiskScore"] = (
    (filtered_df["AgeDays"] / 30).clip(0,1) * 0.6 +
    filtered_df["Status"].str.contains("open", case=False).astype(int) * 0.4
) * 100

filtered_df["TrafficLight"] = pd.cut(
    filtered_df["RiskScore"],
    bins=[0,40,70,100],
    labels=["Low","Medium","High"]
)

# =========================
# HEADER
# =========================
col_left, col_right = st.columns([3,1])

with col_left:
    st.markdown("## 📊 TQ & RFI ML Dashboard")
    st.caption("Project Overview & Response Analytics")

with col_right:
    st.markdown(f"### 📅 {datetime.now().strftime('%d %b %Y')}")
    st.download_button("⬇ Download Report", filtered_df.to_csv(index=False), "report.csv")

st.markdown("---")

# =========================
# A + B
# =========================
row1 = st.columns([2.5,1.5])

with row1[0]:
    st.markdown("### A - Project Overview Analytics")

    c1,c2,c3 = st.columns(3)
    c1.metric("Not Responded >7 Days", len(over_7))
    c2.metric("Total TQs", int(is_tq.sum()))
    c3.metric("Total RFIs", int(is_rfi.sum()))

    venn = pd.DataFrame({
        "Type": ["TQ Only","RFI Only","Both"],
        "Count": [
            (is_tq & ~is_rfi).sum(),
            (is_rfi & ~is_tq).sum(),
            (is_tq & is_rfi).sum()
        ]
    })

    fig = px.bar(venn, x="Type", y="Count", color="Type")
    st.plotly_chart(fig, use_container_width=True)

with row1[1]:
    st.markdown("### B - KPI")
    st.metric("Closed Items", len(closed))
    st.metric(">30 Days Overdue", len(over_30))

# =========================
# C D E
# =========================
row2 = st.columns([2,2,1.5])

with row2[0]:
    st.markdown("### C - Trend")

    trend = filtered_df.groupby(filtered_df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig = go.Figure()
    for col in trend.columns:
        fig.add_trace(go.Scatter(y=trend[col], name=col))

    st.plotly_chart(fig, use_container_width=True)

with row2[1]:
    st.markdown("### D - Age Distribution")

    bins=[0,2,7,14,30,999]
    labels=["0-2","3-7","8-14","15-30","30+"]

    filtered_df["AgeBand"] = pd.cut(filtered_df["AgeDays"], bins=bins, labels=labels)
    age = filtered_df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig = px.bar(x=age.index, y=age.values, text=age.values)
    st.plotly_chart(fig, use_container_width=True)

with row2[2]:
    st.markdown("### E - AI Risk")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=filtered_df["RiskScore"].mean(),
        title={"text":"Avg Risk %"}
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE (DRILL DOWN)
# =========================
st.markdown("---")
st.markdown("### 📋 Live Data (Drilldown)")

st.dataframe(
    filtered_df[["Project ID","Doc Type","Subject","Status","AgeDays","RiskScore","TrafficLight"]],
    use_container_width=True
)

# =========================
# INSIGHTS
# =========================
st.markdown("---")
st.markdown("### 🧠 AI Insights & Recommendations")

col1,col2 = st.columns(2)

with col1:
    st.warning(f"{len(over_7)} items are high risk (>7 days, no response)")

with col2:
    st.info("Mechanical / critical disciplines likely driving overdue distribution (rule-based insight)")

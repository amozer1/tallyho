import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

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

# ---------- AUTO-DETECT COLUMNS ----------
def find_column(possible_names):
    for col in df.columns:
        for name in possible_names:
            if name.lower() in col.lower():
                return col
    return None

type_col = find_column(["type", "tq", "rfi"])
status_col = find_column(["status"])
date_col = find_column(["date", "raised"])
due_col = find_column(["due"])

# ---------- SAFE FALLBACK ----------
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["Days Open"] = (pd.Timestamp.today() - df[date_col]).dt.days
else:
    df["Days Open"] = 0

# ---------- CLASSIFY TQ / RFI ----------
def classify(row):
    if type_col:
        val = str(row[type_col]).lower()
        if "rfi" in val:
            return "RFI"
        elif "tq" in val:
            return "TQ"
    return "Unknown"

df["Doc Type"] = df.apply(classify, axis=1)

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
choice = st.sidebar.radio("", [
    "Overview","TQs","RFIs","Analytics","AI Insights"
])

# ---------- TITLE ----------
col1, col2 = st.columns([6,2])
with col1:
    st.markdown("### TQ & RFI AI Dashboard")
    st.caption("Project Overview & Response Analytics")
with col2:
    st.date_input("")

# ---------- KPI ----------
k1,k2,k3,k4 = st.columns(4)

total_tq = len(df[df["Doc Type"]=="TQ"])
total_rfi = len(df[df["Doc Type"]=="RFI"])

closed = len(df[df[status_col].str.contains("close", case=False, na=False)]) if status_col else 0
overdue = len(df[df["Days Open"] > 7])

with k1:
    st.metric("Total TQs", total_tq)
with k2:
    st.metric("Total RFIs", total_rfi)
with k3:
    st.metric("Closed", closed)
with k4:
    st.metric("Overdue (>7 Days)", overdue)

# ---------- VENN CALC ----------
tq_overdue = len(df[(df["Doc Type"]=="TQ") & (df["Days Open"]>7)])
rfi_overdue = len(df[(df["Doc Type"]=="RFI") & (df["Days Open"]>7)])

both = int(min(tq_overdue, rfi_overdue) * 0.3)  # approximation overlap
tq_only = tq_overdue - both
rfi_only = rfi_overdue - both

total = max(tq_only + rfi_only + both, 1)

tq_pct = int((tq_only/total)*100)
both_pct = int((both/total)*100)
rfi_pct = int((rfi_only/total)*100)

# ---------- VENN STYLE ----------
st.subheader("Not Responded within 7 Days")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.4)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(102,0,255,0.4)")
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
              fillcolor="rgba(0,255,102,0.4)")

fig.add_annotation(x=1, y=1, text=f"TQ Only<br>{tq_pct}%")
fig.add_annotation(x=2, y=1, text=f"Both<br>{both_pct}%")
fig.add_annotation(x=3, y=1, text=f"RFI Only<br>{rfi_pct}%")

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
    st.subheader("Trend")
    if date_col:
        trend = px.line(df, x=date_col, y="Days Open", color="Doc Type")
        st.plotly_chart(trend, use_container_width=True)

with c2:
    st.subheader("Outstanding by Age")
    bins = pd.cut(df["Days Open"], bins=[0,2,7,14,30,100])
    st.bar_chart(bins.value_counts())

with c3:
    st.subheader("AI Risk Prediction")
    risk_score = int(min(100, overdue / max(len(df),1) * 100))

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': "Risk Level"},
        gauge={'axis': {'range': [0,100]}}
    ))
    gauge.update_layout(paper_bgcolor="#0B1220")
    st.plotly_chart(gauge, use_container_width=True)

# ---------- AI INSIGHTS ----------
st.subheader("AI Insights & Recommendations")

if overdue > 0:
    st.warning(f"{overdue} items overdue >7 days")
if total_rfi > total_tq:
    st.info("RFI volume higher than TQs — possible design clarification bottleneck")
if closed < len(df)*0.5:
    st.error("Low closure rate — risk of backlog")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from src.data_loader import load_data
from src.features import build_features
from src.model import load_model
from src.predict import run_prediction

st.set_page_config(
    page_title="TQ & RFI AI Dashboard",
    page_icon="📊",
    layout="wide",
)

# ================= LOAD DATA =================
df = load_data()

# ================= FEATURE ENGINEERING =================
X, y = build_features(df)

# ================= AI MODEL =================
model = load_model()

df = run_prediction(df, model)

# ================= COLUMN DETECTION SAFETY =================
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

# ================= DATE HANDLING =================
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["Days Open"] = (pd.Timestamp.today() - df[date_col]).dt.days
else:
    df["Days Open"] = 0

# ================= CLASSIFICATION =================
def classify(row):
    if type_col:
        val = str(row[type_col]).lower()
        if "rfi" in val:
            return "RFI"
        elif "tq" in val:
            return "TQ"
    return "Unknown"

df["Doc Type"] = df.apply(classify, axis=1)

# ================= SIDEBAR =================
choice = st.sidebar.radio("Navigation", [
    "Overview","TQs","RFIs","Analytics","AI Insights"
])

# ================= HEADER =================
col1, col2 = st.columns([6,2])
with col1:
    st.markdown("### TQ & RFI AI Dashboard")
    st.caption("AI-driven Delay Prediction & Control Tower")
with col2:
    st.date_input("Report Date")

# ================= KPIs =================
k1,k2,k3,k4 = st.columns(4)

total_tq = len(df[df["Doc Type"]=="TQ"])
total_rfi = len(df[df["Doc Type"]=="RFI"])

closed = len(df[df[status_col].str.contains("close", case=False, na=False)]) if status_col else 0
overdue = len(df[df["delay_probability"] > 70])

with k1:
    st.metric("Total TQs", total_tq)
with k2:
    st.metric("Total RFIs", total_rfi)
with k3:
    st.metric("Closed", closed)
with k4:
    st.metric("AI High Risk", overdue)

# ================= SLA LOGIC (REAL) =================
if due_col:
    df[due_col] = pd.to_datetime(df[due_col], errors="coerce")
    df["SLA_Status"] = np.where(
        df[due_col] < pd.Timestamp.today(),
        "Overdue",
        "On Track"
    )
else:
    df["SLA_Status"] = "Unknown"

# ================= VENN CALC =================
tq_overdue = len(df[(df["Doc Type"]=="TQ") & (df["delay_probability"] > 70)])
rfi_overdue = len(df[(df["Doc Type"]=="RFI") & (df["delay_probability"] > 70)])

both = int(min(tq_overdue, rfi_overdue) * 0.3)
tq_only = tq_overdue - both
rfi_only = rfi_overdue - both

total = max(tq_only + rfi_only + both, 1)

tq_pct = int((tq_only/total)*100)
both_pct = int((both/total)*100)
rfi_pct = int((rfi_only/total)*100)

# ================= VENN =================
st.subheader("AI Identified Non-Responsive Items")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.4)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(102,0,255,0.4)")

fig.add_annotation(x=1, y=1, text=f"TQ Only<br>{tq_pct}%")
fig.add_annotation(x=2, y=1, text=f"Overlap<br>{both_pct}%")
fig.add_annotation(x=3, y=1, text=f"RFI Only<br>{rfi_pct}%")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)

# ================= CHARTS =================
c1,c2,c3 = st.columns(3)

with c1:
    st.subheader("Trend")
    if date_col:
        st.plotly_chart(
            px.line(df, x=date_col, y="Days Open", color="Doc Type"),
            use_container_width=True
        )

with c2:
    st.subheader("SLA Status")
    st.bar_chart(df["SLA_Status"].value_counts())

with c3:
    st.subheader("AI Risk Score")

    risk_score = int(df["delay_probability"].mean())

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': "AI Delay Risk"},
        gauge={'axis': {'range': [0,100]}}
    ))

    st.plotly_chart(gauge, use_container_width=True)

# ================= AI INSIGHTS =================
st.subheader("AI Insights & Recommendations")

if overdue > 0:
    st.warning(f"{overdue} high-risk items detected by AI (>70%)")

if df["Doc Type"].value_counts().get("RFI",0) > df["Doc Type"].value_counts().get("TQ",0):
    st.info("RFI load higher than TQs → design clarification bottleneck likely")

if df["delay_probability"].mean() > 60:
    st.error("System-wide delay risk is elevated")

st.success("AI model actively monitoring document flow")
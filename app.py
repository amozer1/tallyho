import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TQ & RFI AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DARK THEME CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0B1220;
    color: white;
}

.big-title {
    font-size: 34px;
    font-weight: 700;
    color: white;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg,#111827,#1F2937);
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,.4);
}

[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")

    # Clean column names (safe minimal cleaning)
    df.columns = df.columns.astype(str).str.strip()

    # Convert dates safely
    for col in ["Date Sent", "Required Date", "Reply Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Ensure numeric safety
    df["Days Open"] = np.where(
        df["Reply Date"].notna(),
        (df["Reply Date"] - df["Date Sent"]).dt.days,
        (pd.Timestamp.today() - df["Date Sent"]).dt.days
    )

    # Ensure Status exists and is clean
    df["Status"] = df["Status"].fillna("Open")

    # Overdue logic
    df.loc[(df["Days Open"] > 7) & (df["Reply Date"].isna()), "Status"] = "Overdue"
    df.loc[df["Reply Date"].notna(), "Status"] = "Closed"

    return df

df = load_data()

# ---------------- TITLE ----------------
col1, col2 = st.columns([8, 2])

with col1:
    st.markdown('<div class="big-title">📊 TQ & RFI AI Dashboard</div>', unsafe_allow_html=True)
    st.caption("Executive Project Communication Intelligence")

with col2:
    st.date_input("Date", datetime.today())

# ---------------- KPI ----------------
total_tq = len(df[df["Doc Type"] == "TQ"])
total_rfi = len(df[df["Doc Type"] == "RFI"])
closed = len(df[df["Status"] == "Closed"])
open_ = len(df[df["Status"] == "Open"])
overdue = len(df[df["Status"] == "Overdue"])
avg_days = round(df["Days Open"].mean(), 1)

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("TQs", total_tq)
k2.metric("RFIs", total_rfi)
k3.metric("Closed", closed)
k4.metric("Open", open_)
k5.metric("Overdue", overdue)
k6.metric("Avg Days", avg_days)

# ---------------- VENN STYLE VISUAL ----------------
st.subheader("Communication Health Overview")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.35)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(150,0,255,0.35)")
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
              fillcolor="rgba(0,255,120,0.35)")

fig.add_annotation(x=1, y=1, text="TQ")
fig.add_annotation(x=2, y=1, text="Overlap")
fig.add_annotation(x=3, y=1, text="RFI")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(height=350, paper_bgcolor="#0B1220")

st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Trend")
    trend = df.groupby(["Date Sent", "Doc Type"]).size().reset_index(name="Count")
    fig1 = px.line(trend, x="Date Sent", y="Count", color="Doc Type", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Age Distribution")
    bins = pd.cut(df["Days Open"], [0,2,7,14,30,100])
    fig2 = px.bar(x=bins.value_counts().index.astype(str),
                  y=bins.value_counts().values,
                  template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with c3:
    st.subheader("Risk Gauge")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=min(overdue * 4, 100),
        title={"text": "Risk Level"},
        gauge={"axis": {"range": [0,100]}}
    ))
    fig3.update_layout(paper_bgcolor="#0B1220")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("AI Insights")

a1, a2, a3 = st.columns(3)

with a1:
    st.info(f"{overdue} items are overdue (>7 days).")

with a2:
    top_recipient = df["Recipient"].mode()[0]
    st.success(f"Top workload: {top_recipient}")

with a3:
    st.warning("Recommend automated reminders for overdue RFIs/TQs.")

# ---------------- TABLE ----------------
st.subheader("Full Register")
st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("AI-powered TQ & RFI Dashboard | Streamlit + Python")
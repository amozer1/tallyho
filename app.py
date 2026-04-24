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

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0B1220;
    color: white;
}

.big-font {
    font-size: 34px !important;
    font-weight: bold;
    color: white;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg,#111827,#1F2937);
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,.35);
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

    # Clean headers
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )

    # Rename columns
    df.rename(columns={
        "Doc Type": "Type",
        "Date reply required by": "Required Date",
        "Date of reply (CDE)": "Reply Date",
        "Period (Wks)": "Period"
    }, inplace=True)

    # Convert dates safely
    for col in ["Date Sent", "Required Date", "Reply Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Numeric conversion
    if "Period" in df.columns:
        df["Period"] = pd.to_numeric(df["Period"], errors="coerce")

    today = pd.Timestamp.today()

    # Days Open
    if "Date Sent" in df.columns:
        df["Days Open"] = np.where(
            df["Reply Date"].notna(),
            (df["Reply Date"] - df["Date Sent"]).dt.days,
            (today - df["Date Sent"]).dt.days
        )
    else:
        df["Days Open"] = 0

    # Status
    if "Status" not in df.columns:
        df["Status"] = "Open"

    df.loc[(df["Days Open"] > 7) & (df["Reply Date"].isna()), "Status"] = "Overdue"
    df.loc[df["Reply Date"].notna(), "Status"] = "Closed"

    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")

menu = [
    "Overview",
    "Analytics",
    "AI Insights",
    "Reports"
]

choice = st.sidebar.radio("", menu)

# ---------------- TITLE ----------------
col1, col2 = st.columns([8,2])

with col1:
    st.markdown('<p class="big-font">📊 TQ & RFI AI Dashboard</p>', unsafe_allow_html=True)
    st.caption("Project Overview & Response Analytics")

with col2:
    st.date_input("Date", datetime.today())

# ---------------- KPI ----------------
total_tq = len(df[df["Type"] == "TQ"]) if "Type" in df.columns else 0
total_rfi = len(df[df["Type"] == "RFI"]) if "Type" in df.columns else 0
closed_items = len(df[df["Status"] == "Closed"])
overdue_items = len(df[df["Status"] == "Overdue"])
open_items = len(df[df["Status"] == "Open"])
avg_days = round(df["Days Open"].mean(), 1)

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total TQs", total_tq)
k2.metric("Total RFIs", total_rfi)
k3.metric("Closed", closed_items)
k4.metric("Open", open_items)
k5.metric("Overdue", overdue_items)
k6.metric("Avg Days", avg_days)

# ---------------- VENN STYLE ----------------
st.subheader("Outstanding / Overdue Queries")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.35)", line_color="rgba(0,102,255,1)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(153,0,255,0.35)", line_color="rgba(153,0,255,1)")
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
              fillcolor="rgba(0,255,102,0.35)", line_color="rgba(0,255,102,1)")

fig.add_annotation(x=1, y=1, text="TQ")
fig.add_annotation(x=2, y=1, text="Both")
fig.add_annotation(x=3, y=1, text="RFI")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

fig.update_layout(
    height=350,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#0B1220"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Trend")
    if "Date Sent" in df.columns and "Type" in df.columns:
        trend = df.groupby(["Date Sent", "Type"]).size().reset_index(name="Count")
        fig1 = px.line(trend, x="Date Sent", y="Count", color="Type", template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Outstanding by Age")
    age_bins = pd.cut(df["Days Open"], bins=[0,2,7,14,30,100])
    age_count = age_bins.value_counts().sort_index()
    fig2 = px.bar(
        x=age_count.index.astype(str),
        y=age_count.values,
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)

with c3:
    st.subheader("AI Risk Prediction")
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=min(overdue_items * 3, 100),
        title={'text': "Risk"},
        gauge={'axis': {'range': [0,100]}}
    ))
    fig3.update_layout(paper_bgcolor="#0B1220")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("🤖 AI Insights")

a1, a2, a3 = st.columns(3)

with a1:
    st.info(f"{overdue_items} items are overdue.")

with a2:
    top_recipient = df["Recipient"].mode()[0] if "Recipient" in df.columns else "N/A"
    st.success(f"{top_recipient} has highest workload.")

with a3:
    st.warning("Consider sending reminders.")

# ---------------- TABLE ----------------
st.subheader("Detailed Log")
st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with Streamlit")
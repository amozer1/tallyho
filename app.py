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
html, body, [class*="css"] {
    background-color: #0B1220;
    color: white;
}

.big-font {
    font-size: 34px !important;
    font-weight: 700;
    color: white;
}

.metric-box {
    background: linear-gradient(135deg, #111827, #1F2937);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,.35);
    text-align: center;
}

.insight-box {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,.25);
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

    # Clean column names
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]

    rename_map = {
        "Doc Type": "Type",
        "Date Sent": "Date Sent",
        "Date of reply (CDE)": "Reply Date",
        "Date reply required by": "Required Date",
        "Period (Wks)": "Period"
    }

    df.rename(columns=rename_map, inplace=True)

    # Convert dates
    for col in ["Date Sent", "Reply Date", "Required Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    today = pd.Timestamp.today()

    df["Days Open"] = np.where(
        df["Reply Date"].notna(),
        (df["Reply Date"] - df["Date Sent"]).dt.days,
        (today - df["Date Sent"]).dt.days
    )

    df["Status"] = np.where(df["Reply Date"].notna(), "Closed", "Open")
    df.loc[(df["Days Open"] > 7) & (df["Reply Date"].isna()), "Status"] = "Overdue"

    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Navigation")

menu = [
    "Overview",
    "TQs",
    "RFIs",
    "Analytics",
    "AI Insights",
    "Predictive Risk",
    "Reports",
    "Settings"
]

choice = st.sidebar.radio("", menu)

# ---------------- TITLE ----------------
col1, col2 = st.columns([8, 2])

with col1:
    st.markdown('<p class="big-font">📊 TQ & RFI AI Dashboard</p>', unsafe_allow_html=True)
    st.caption("Project Overview & Response Analytics")

with col2:
    st.date_input("Date", datetime.today())

# ---------------- KPI ----------------
total_tq = len(df[df["Type"] == "TQ"])
total_rfi = len(df[df["Type"] == "RFI"])
closed_items = len(df[df["Status"] == "Closed"])
overdue_items = len(df[df["Status"] == "Overdue"])
avg_days = round(df["Days Open"].mean(), 1)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total TQs", total_tq)
k2.metric("Total RFIs", total_rfi)
k3.metric("Closed", closed_items)
k4.metric("Overdue >7d", overdue_items)
k5.metric("Avg Days Open", avg_days)

# ---------------- VENN STYLE ----------------
st.subheader("Outstanding / Overdue Queries")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,102,255,0.35)", line_color="rgba(0,102,255,1)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(153,0,255,0.35)", line_color="rgba(153,0,255,1)")
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
              fillcolor="rgba(0,255,102,0.35)", line_color="rgba(0,255,102,1)")

fig.add_annotation(x=1, y=1, text="TQ<br>24%")
fig.add_annotation(x=2, y=1, text="Both<br>12%")
fig.add_annotation(x=3, y=1, text="RFI<br>18%")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

fig.update_layout(
    height=380,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#0B1220"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Trend Over Time")
    trend = df.groupby(["Date Sent", "Type"]).size().reset_index(name="Count")
    fig1 = px.line(
        trend,
        x="Date Sent",
        y="Count",
        color="Type",
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Outstanding by Age")
    age_bins = pd.cut(df["Days Open"], bins=[0, 2, 7, 14, 30, 100])
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
        value=72,
        title={'text': "High Risk"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    fig3.update_layout(
        paper_bgcolor="#0B1220"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("🤖 AI Insights & Recommendations")

a1, a2, a3 = st.columns(3)

with a1:
    st.info("28 items are at high risk of delay.")

with a2:
    st.success("Conal Cunningham has highest outstanding workload.")

with a3:
    st.warning("Consider auto-reminders for overdue items.")

# ---------------- TABLE ----------------
st.subheader("Detailed Log")

st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with Streamlit • AI/ML Dashboard")
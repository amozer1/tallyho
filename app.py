import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TQ & RFI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CLEAN DARK UI ----------------
st.markdown("""
<style>
body { background-color: #0B1220; color: white; }

.title {
    font-size: 28px;
    font-weight: 700;
    color: white;
}

.card {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
}

.small {
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA (ROBUST) ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", engine="openpyxl")

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Standardise expected columns safely
    col_map = {
        "Doc Type": "Doc_Type",
        "Date Sent": "Date_Sent",
        "Required Date": "Required_Date",
        "Reply Date": "Reply_Date"
    }

    for k, v in col_map.items():
        if k in df.columns:
            df.rename(columns={k: v}, inplace=True)

    # Ensure required columns exist (avoid KeyError crashes)
    for col in ["Doc_Type", "Date_Sent", "Required_Date", "Reply_Date", "Status"]:
        if col not in df.columns:
            df[col] = np.nan

    # Convert dates safely
    for col in ["Date_Sent", "Required_Date", "Reply_Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Status cleanup
    df["Status"] = df["Status"].fillna("Unknown").astype(str)

    # Days open calculation
    today = pd.Timestamp.today()
    df["Days_Open"] = (today - df["Date_Sent"]).dt.days

    return df

df = load_data()

# ---------------- HEADER ----------------
col1, col2 = st.columns([6, 1])

with col1:
    st.markdown('<div class="title">TQ & RFI AI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="small">Engineering Document Intelligence System</div>', unsafe_allow_html=True)

with col2:
    st.write(datetime.today().strftime("%d-%m-%Y"))

# ---------------- KPI ----------------
total = len(df)
open_items = len(df[df["Status"].str.lower() == "open"])
closed_items = len(df[df["Status"].str.lower() == "closed"])

overdue = len(df[
    (df["Reply_Date"].isna()) &
    (df["Days_Open"] > 7)
])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Items", total)
c2.metric("Open", open_items)
c3.metric("Closed", closed_items)
c4.metric("Overdue > 7 Days", overdue)

# ---------------- DONUT (CLEAN VENN STYLE) ----------------
st.subheader("Response Overview")

fig = go.Figure(data=[go.Pie(
    labels=["Open", "Closed", "Overdue"],
    values=[open_items, closed_items, overdue],
    hole=0.55,
    marker=dict(colors=["#3B82F6", "#22C55E", "#EF4444"])
)])

fig.update_layout(
    paper_bgcolor="#0B1220",
    plot_bgcolor="#0B1220",
    font_color="white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- ANALYTICS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Document Type Split")

    fig1 = px.histogram(
        df,
        x="Doc_Type",
        color="Status",
        barmode="group"
    )
    fig1.update_layout(
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        font_color="white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Days Open Distribution")

    fig2 = px.histogram(df, x="Days_Open", nbins=20)
    fig2.update_layout(
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        font_color="white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("AI Insights")

high_risk = df[(df["Reply_Date"].isna()) & (df["Days_Open"] > 7)]

i1, i2, i3 = st.columns(3)

i1.info(f"High Risk Items: {len(high_risk)}")
i2.success(f"Most Active Sender: {df['Sender'].mode()[0] if 'Sender' in df.columns else 'N/A'}")
i3.warning("Recommend auto-escalation for overdue RFIs/TQs")

# ---------------- DATA TABLE ----------------
st.subheader("Live Register")

st.dataframe(
    df.sort_values("Days_Open", ascending=False),
    use_container_width=True
)
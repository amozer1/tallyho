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
    layout="wide"
)

# ---------------- DARK THEME ----------------
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: white;
}

[data-testid="stAppViewContainer"] {
    background-color: #0B1220;
}

[data-testid="metric-container"] {
    background-color: #111827;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")

    # CLEAN HEADERS
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.strip()
    )

    # SAFE COLUMN FINDER
    def find_col(keyword):
        for c in df.columns:
            if keyword.lower() in c.lower():
                return c
        return None

    col_type = find_col("doc type")
    col_sent = find_col("date sent")
    col_reply = find_col("reply date")
    col_req = find_col("required")
    col_sender = find_col("sender")
    col_status = find_col("status")

    # TYPE
    df["Type"] = df[col_type] if col_type else "Unknown"

    # DATE SENT (CRITICAL FIX)
    df["Date Sent"] = pd.to_datetime(
        df[col_sent], errors="coerce", dayfirst=True
    ) if col_sent else pd.NaT

    # REQUIRED DATE
    df["Required Date"] = pd.to_datetime(
        df[col_req], errors="coerce", dayfirst=True
    ) if col_req else pd.NaT

    # REPLY DATE (ALLOW EMPTY CELLS → NaT)
    df["Reply Date"] = pd.to_datetime(
        df[col_reply], errors="coerce", dayfirst=True
    ) if col_reply else pd.NaT

    # SENDER
    df["Sender"] = df[col_sender] if col_sender else "Unknown"

    # STATUS
    df["Status"] = df[col_status].fillna("Open") if col_status else "Open"

    # ---------------- DAYS OPEN ----------------
    today = pd.Timestamp.today()

    df["Days Open"] = np.where(
        df["Reply Date"].notna(),
        (df["Reply Date"] - df["Date Sent"]).dt.days,
        (today - df["Date Sent"]).dt.days
    )

    # ---------------- STATUS LOGIC ----------------
    df.loc[df["Reply Date"].notna(), "Status"] = "Closed"
    df.loc[(df["Reply Date"].isna()) & (df["Days Open"] > 7), "Status"] = "Overdue"

    return df


df = load_data()

# ---------------- TITLE ----------------
st.title("📊 TQ & RFI AI Dashboard")
st.caption("Engineering Communication Intelligence System")

# ---------------- KPIs ----------------
total = len(df)
tq = len(df[df["Type"] == "TQ"])
rfi = len(df[df["Type"] == "RFI"])
closed = len(df[df["Status"] == "Closed"])
open_ = len(df[df["Status"] == "Open"])
overdue = len(df[df["Status"] == "Overdue"])
avg_days = round(df["Days Open"].mean(), 1)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total", total)
c2.metric("TQ", tq)
c3.metric("RFI", rfi)
c4.metric("Closed", closed)
c5.metric("Overdue", overdue)

# ---------------- VENN STYLE VISUAL ----------------
st.subheader("Response Overview")

fig = go.Figure()

fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
              fillcolor="rgba(0,100,255,0.3)")
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
              fillcolor="rgba(180,0,255,0.3)")

fig.add_annotation(x=1, y=1, text="TQ")
fig.add_annotation(x=2, y=1, text="Overlap")
fig.add_annotation(x=3, y=1, text="RFI")

fig.update_layout(height=300, paper_bgcolor="#0B1220")
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Status Split")
    fig1 = px.pie(df, names="Status", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Days Open")
    fig2 = px.histogram(df, x="Days Open", nbins=10, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.subheader("Risk Gauge")
    risk = min(overdue * 5, 100)

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={"text": "Risk Level (%)"},
        gauge={"axis": {"range": [0, 100]}}
    ))

    fig3.update_layout(paper_bgcolor="#0B1220")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("AI Insights")

a1, a2, a3 = st.columns(3)

with a1:
    st.info(f"{overdue} items overdue (>7 days).")

with a2:
    top_sender = df["Sender"].mode()[0] if "Sender" in df.columns else "N/A"
    st.success(f"Top sender: {top_sender}")

with a3:
    st.warning("Introduce automated reminders for overdue RFIs/TQs.")

# ---------------- TABLE ----------------
st.subheader("Full Register")
st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="TQ & RFI ML Dashboard", layout="wide")

# =========================
# LOAD DATA (CLOUD SAFE)
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]
    return df

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

default_path = "data/TQ_TH.xlsx"

if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data(default_path)

# =========================
# CLEANING
# =========================
for c in df.columns:
    df[c] = df[c].astype(str)

df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)
df["Reply Date"] = pd.to_datetime(df["Reply Date"], errors="coerce", dayfirst=True)
df["Required Date"] = pd.to_datetime(df["Required Date"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())

# =========================
# CORE METRICS
# =========================
df["AgeDays"] = (now - df["Date Sent"]).dt.days.fillna(0)

is_tq = df["Doc Type"].str.contains("TQ", na=False)
is_rfi = df["Doc Type"].str.contains("RFI", na=False)

open_items = df[df["Status"].str.contains("Open", case=False, na=False)]
closed_items = df[df["Status"].str.contains("Closed", case=False, na=False)]

over_7 = df[df["AgeDays"] > 7]
over_30 = df[df["AgeDays"] > 30]

# =========================
# HEADER CARDS (TOP LEFT / RIGHT)
# =========================
top_left, top_right = st.columns([3, 1])

with top_left:
    st.title("📊 TQ & RFI ML Dashboard")
    st.caption("Project Overview | Response Analytics | AI Risk Intelligence")

with top_right:
    st.write(f"📅 {datetime.now().strftime('%d %b %Y')}")
    st.download_button("⬇ Download Report", df.to_csv(index=False), "TQ_RFI_Report.csv")

st.markdown("---")

# =========================
# A + B SECTION
# =========================
colA, colB = st.columns([2.6, 1.4])

# -------------------------
# A - OVERVIEW ANALYTICS
# -------------------------
with colA:
    st.subheader("A - Project Overview Analytics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Not Responded >7 Days", len(over_7))
    c2.metric("TQ Total", int(is_tq.sum()))
    c3.metric("RFI Total", int(is_rfi.sum()))

    # Venn-style approximation (clean pie version)
    venn = pd.DataFrame({
        "Type": ["TQ Only", "RFI Only", "Both"],
        "Count": [
            (is_tq & ~is_rfi).sum(),
            (is_rfi & ~is_tq).sum(),
            (is_tq & is_rfi).sum()
        ]
    })

    fig = px.pie(
        venn,
        names="Type",
        values="Count",
        hole=0.55,
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Outstanding Breakdown")

    st.write(f"🔴 TQ Not Responded: {(is_tq & (df['AgeDays'] > 7)).sum()}")
    st.write(f"🟠 RFI Not Responded: {(is_rfi & (df['AgeDays'] > 7)).sum()}")
    st.write(f"🟡 Both Overdue: {(is_tq & is_rfi & (df['AgeDays'] > 7)).sum()}")
    st.write(f"⚠ Total Outstanding >7 Days: {len(over_7)}")

# -------------------------
# B - KPI CARDS
# -------------------------
with colB:
    st.subheader("B - KPI Summary")

    st.metric("Total Open", len(open_items))
    st.metric("Closed Items", len(closed_items))
    st.metric(">30 Days Overdue", len(over_30))

    st.markdown("#### Trend vs 30 Days Baseline")
    st.progress(min(len(over_30) / len(df), 1.0))

# =========================
# C + D + E SECTION
# =========================
row2 = st.columns([2.2, 2.2, 1.6])

# -------------------------
# C - TREND ANALYSIS
# -------------------------
with row2[0]:
    st.subheader("C - TQ & RFI Trend")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig = go.Figure()

    if "TQ" in trend.columns:
        fig.add_trace(go.Scatter(y=trend["TQ"], name="TQ Created", mode="lines+markers"))

    if "RFI" in trend.columns:
        fig.add_trace(go.Scatter(y=trend["RFI"], name="RFI Created", mode="lines+markers"))

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# D - AGE DISTRIBUTION
# -------------------------
with row2[1]:
    st.subheader("D - Outstanding by Age")

    bins = [0, 2, 7, 14, 30, 999]
    labels = ["0-2", "3-7", "8-14", "15-30", "30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig = px.bar(
        x=age.index,
        y=age.values,
        text=[f"{v} ({round(v/len(df)*100,1)}%)" for v in age.values]
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# E - AI RISK (SEMI GAUGE STYLE)
# -------------------------
with row2[2]:
    st.subheader("E - AI Risk Prediction")

    risk_score = (len(over_7) / len(df)) * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        title={"text": "Delay Risk %"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkred"},
            "steps": [
                {"range": [0, 40], "color": "green"},
                {"range": [40, 70], "color": "orange"},
                {"range": [70, 100], "color": "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHTS (BOTTOM SECTION)
# =========================
st.markdown("---")
st.subheader("🧠 AI Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.warning(
        f"⚠ {len(over_7)} items are high risk (>7 days). These require immediate attention due to lack of response."
    )

with col2:
    top_sender = df["Sender"].value_counts().idxmax()
    st.info(
        f"📌 Highest workload sender: {top_sender}. This contributor is driving most document traffic."
    )
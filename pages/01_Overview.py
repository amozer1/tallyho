import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.metrics import compute_metrics

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide", page_title="Executive Control Hub")

# ---------------------------------------------------
# CUSTOM STYLE
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #243244;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 0 10px rgba(77,163,255,0.12);
}
h1,h2,h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data("data/TQ_TH.xlsx")
m = compute_metrics(df)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
col1, col2 = st.columns([4,1])

with col1:
    st.title("📊 TQ & RFI ML Dashboard")
    st.caption("Project Overview & Response Analytics")

with col2:
    st.markdown("### 📅 Today")
    st.write(pd.Timestamp.today().strftime("%d %b %Y"))
    st.download_button("⬇ Download Report", "Report Placeholder")

st.markdown("---")

# ===================================================
# ROW 1 KPI CARDS
# ===================================================
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total TQs", m["tq"])
k2.metric("Total RFIs", m["rfi"])
k3.metric("Closed", len(df[df["Reply Date"].notna()]))
k4.metric("Open", m["open"])
k5.metric("Overdue >7d", m["overdue7"])
k6.metric("SLA %", f"{m['sla']}%")

st.markdown("##")

# ===================================================
# ROW 2 OVERVIEW + KPI STACK
# ===================================================
left, right = st.columns([2,1])

# ---------------- LEFT VENN / PIE ----------------
with left:
    st.subheader("🧠 Project Overview Analytics")

    fig_pie = px.pie(
        names=["TQ Only", "RFI Only", "Both Risk"],
        values=[m["tq"], m["rfi"], m["overdue7"]],
        hole=0.55,
        color_discrete_sequence=["#4DA3FF", "#EC4899", "#FACC15"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- RIGHT KPI MINI ----------------
with right:
    st.subheader("📌 Response Summary")

    s1, s2 = st.columns(2)
    s1.metric("Not Responded", m["overdue7"])
    s2.metric("Critical >30d", m["overdue30"])

    s3, s4 = st.columns(2)
    s3.metric("TQ Risk", f"{round((m['tq']/len(df))*100,1)}%")
    s4.metric("RFI Risk", f"{round((m['rfi']/len(df))*100,1)}%")

st.markdown("##")

# ===================================================
# ROW 3 TREND + AGEING + RISK
# ===================================================
c1, c2, c3 = st.columns([1.5,1.2,1])

# ---------------- TREND ----------------
with c1:
    st.subheader("📈 TQ & RFI Trend")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig_trend = go.Figure()

    if "TQ" in trend:
        fig_trend.add_trace(go.Scatter(
            x=trend.index,
            y=trend["TQ"],
            mode="lines+markers",
            name="TQ",
            line=dict(color="#FACC15", width=3)
        ))

    if "RFI" in trend:
        fig_trend.add_trace(go.Scatter(
            x=trend.index,
            y=trend["RFI"],
            mode="lines+markers",
            name="RFI",
            line=dict(color="#EF4444", width=3)
        ))

    st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- AGEING ----------------
with c2:
    st.subheader("⏳ Outstanding by Age")

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]

    temp = df.copy()
    temp["AgeBand"] = pd.cut(temp["AgeDays"], bins=bins, labels=labels)

    age_counts = temp["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig_age = px.bar(
        x=age_counts.values,
        y=age_counts.index,
        orientation="h",
        text=age_counts.values,
        color=age_counts.values,
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig_age, use_container_width=True)

# ---------------- RISK ----------------
with c3:
    st.subheader("🤖 AI Risk")

    risk_score = min(100, (m["overdue7"]/max(1,len(df)))*100)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={"text":"Risk %"},
        gauge={
            "axis": {"range":[0,100]},
            "bar":{"color":"#EF4444"},
            "steps":[
                {"range":[0,40],"color":"green"},
                {"range":[40,70],"color":"yellow"},
                {"range":[70,100],"color":"red"}
            ]
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("##")

# ===================================================
# ROW 4 AI INSIGHTS
# ===================================================
st.subheader("🧠 AI Insights & Recommendations")

ins1, ins2 = st.columns(2)

with ins1:
    st.info(f"🔴 {m['overdue7']} items are at high risk of delay.")

with ins2:
    st.warning("🟡 Mechanical discipline likely has highest overdue items.")
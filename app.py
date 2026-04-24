import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    return df

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(uploaded_file) if uploaded_file else load_data("data/TQ_TH.xlsx")

# =========================
# CLEAN
# =========================
df["Date Sent"] = pd.to_datetime(df["Date Sent"], errors="coerce", dayfirst=True)

now = pd.Timestamp(datetime.now())
df["AgeDays"] = (now - df["Date Sent"]).dt.days

df["Doc Type"] = df["Doc Type"].str.upper()

tq = df[df["Doc Type"] == "TQ"]
rfi = df[df["Doc Type"] == "RFI"]
overdue = df[df["AgeDays"] > 7]

risk = round(len(overdue)/len(df)*100,1)

# =========================
# GLOBAL STYLE (CONTROL ROOM LOOK)
# =========================
st.markdown("""
<style>

html, body, [class*="css"]  {
    background-color: #0b1220;
    color: #e5e7eb;
    font-family: Arial;
}

/* KPI CARDS */
.kpi {
    background: #111827;
    padding: 8px;
    border-radius: 8px;
    text-align: center;
    font-size: 13px;
    border: 1px solid #1f2937;
}

/* SECTION BOX */
.box {
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 6px;
    background: #0f172a;
}

/* REDUCE SPACE */
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
}

h1, h2, h3 {
    margin: 0px;
    font-size: 16px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("TQ & RFI CONTROL CENTRE")
st.caption(f"Live Engineering Dashboard | {datetime.now().strftime('%d %b %Y %H:%M')}")

# =========================
# KPI ROW (VERY COMPACT)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='kpi'>OVERDUE<br><b>{len(overdue)}</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi'>TQ<br><b>{len(tq)}</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi'>RFI<br><b>{len(rfi)}</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='kpi'>RISK %<br><b>{risk}</b></div>", unsafe_allow_html=True)

# =========================
# MAIN GRID
# =========================
left, right = st.columns([2, 1])

# =========================
# LEFT SIDE (A + C)
# =========================
with left:

    st.markdown("### A - Overview")

    pie = px.pie(
        names=["TQ","RFI"],
        values=[len(tq), len(rfi)],
        hole=0.6
    )
    pie.update_layout(height=250, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(pie, use_container_width=True)

    st.markdown("### C - Trend")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig = go.Figure()
    if "TQ" in trend:
        fig.add_trace(go.Scatter(y=trend["TQ"], name="TQ"))
    if "RFI" in trend:
        fig.add_trace(go.Scatter(y=trend["RFI"], name="RFI"))

    fig.update_layout(height=250, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# RIGHT SIDE (B + D + E)
# =========================
with right:

    st.markdown("### B - KPIs")

    st.metric("Overdue >30", len(df[df["AgeDays"] > 30]))
    st.metric("Open Items", len(df[df["Status"].str.upper()=="OPEN"]))

    st.markdown("---")

    st.markdown("### D - Ageing")

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig2 = px.bar(x=age.index, y=age.values)
    fig2.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### E - Risk")

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        gauge={"axis":{"range":[0,100]}}
    ))

    fig3.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# LIVE REGISTER (ONLY SCROLLABLE PART)
# =========================
st.markdown("---")

st.markdown("### 📋 Live Register")

st.dataframe(
    df[[
        "Doc Type",
        "Seq No",
        "Sender",
        "Recipient",
        "Status",
        "AgeDays"
    ]],
    use_container_width=True,
    height=250
)
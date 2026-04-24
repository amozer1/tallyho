import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.metrics import compute_metrics
from utils.theme import *

st.set_page_config(layout="wide")

# ================= THEME =================
st.markdown(f"""
<style>
.block-container {{
    padding: 1rem 2rem;
}}

[data-testid="stMetric"] {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0px 0px 10px rgba(77,163,255,0.15);
    color: {TEXT};
}}
</style>
""", unsafe_allow_html=True)


# ================= DATA =================
file = st.file_uploader("Upload Excel", type=["xlsx"])
df = load_data(file) if file else load_data("data/TQ_TH.xlsx")

m = compute_metrics(df)


# ================= KPI COLOUR METRICS =================
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("TQs", m["tq"], delta_color="off")
c2.metric("RFIs", m["rfi"], delta_color="off")

c3.metric("Open Items", m["open"], delta_color="inverse")

c4.metric("Overdue >7d", m["overdue7"], delta_color="inverse")

c5.metric("SLA %", f"{m['sla']}%", delta_color="normal")

st.markdown("---")


# ================= MAIN GRID =================
left, right = st.columns([2,1])


# ================= LEFT =================
with left:

    st.subheader("🟣 TQ vs RFI Intelligence")

    fig = px.pie(
        names=["TQ", "RFI"],
        values=[m["tq"], m["rfi"]],
        hole=0.6,
        color_discrete_sequence=[BLUE, PINK]
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("📊 Communication Trend")

    trend = m["df"].groupby(m["df"]["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig2 = go.Figure()

    if "TQ" in trend:
        fig2.add_trace(go.Scatter(
            y=trend["TQ"],
            name="TQ",
            line=dict(color=YELLOW, width=3)
        ))

    if "RFI" in trend:
        fig2.add_trace(go.Scatter(
            y=trend["RFI"],
            name="RFI",
            line=dict(color=RED, width=3)
        ))

    st.plotly_chart(fig2, use_container_width=True)


# ================= RIGHT =================
with right:

    st.subheader("🧠 Ageing Heat Map")

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]

    temp = m["df"].copy()
    temp["AgeBand"] = pd.cut(temp["AgeDays"], bins=bins, labels=labels)

    age_counts = temp["AgeBand"].value_counts().reindex(labels).fillna(0)

    st.bar_chart(age_counts)

    st.markdown("")

    st.subheader("⚠ Risk Summary")

    st.metric("Critical (>30d)", m["overdue30"], delta_color="inverse")
    st.metric("Warning (>7d)", m["overdue7"], delta_color="inverse")
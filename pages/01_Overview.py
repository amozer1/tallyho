import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data
from utils.metrics import compute_metrics

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(layout="wide", page_title="Executive Dashboard")

# ------------------------------------------------
# DATA
# ------------------------------------------------
df = load_data()
m = compute_metrics(df)

# ------------------------------------------------
# COLORS
# ------------------------------------------------
BG = "#081226"
CARD = "#111827"
BORDER = "#1f2937"
BLUE = "#2F80ED"
PURPLE = "#9B51E0"
GREEN = "#27AE60"
RED = "#EB5757"
YELLOW = "#F2C94C"
CYAN = "#00C2FF"

# ------------------------------------------------
# STYLE
# ------------------------------------------------
st.markdown(f"""
<style>
body {{
    background-color:{BG};
}}
.block-container {{
    padding-top:0.5rem;
    padding-bottom:0.5rem;
    max-width: 100%;
}}

.card {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:18px;
    padding:15px;
    box-shadow: 0 0 8px rgba(0,0,0,0.4);
    margin-bottom:12px;
}}

.small-card {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:14px;
    padding:12px;
    text-align:center;
}}

.title {{
    font-size:34px;
    font-weight:700;
    color:white;
}}

.subtitle {{
    font-size:16px;
    color:#9ca3af;
}}

.metric-title {{
    color:#aaa;
    font-size:14px;
}}

.metric-value {{
    color:white;
    font-size:34px;
    font-weight:bold;
}}
</style>
""", unsafe_allow_html=True)

# ====================================================
# HEADER
# ====================================================
h1, h2, h3 = st.columns([5,2,2])

with h1:
    st.markdown(f"""
    <div class="card">
        <div class="title">TQ & RFI ML Dashboard</div>
        <div class="subtitle">Project overview and Response analytics</div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div class="card">
        <div style="font-size:22px;">📅</div>
        <b>{pd.Timestamp.today().strftime("%d %b %Y")}</b><br>
        {pd.Timestamp.today().strftime("%A")}
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.download_button("⬇ Download Report", data="report")

# ====================================================
# ROW 2
# ====================================================
left, right = st.columns([2,2])

# ---------------- A ----------------
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("A  Project Overview Analytics")

    a1, a2 = st.columns([2,1])

    with a1:
        fig = go.Figure()

        fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
                      fillcolor="rgba(47,128,237,0.35)", line_color=BLUE)
        fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
                      fillcolor="rgba(0,194,255,0.35)", line_color=CYAN)
        fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
                      fillcolor="rgba(155,81,224,0.35)", line_color=PURPLE)

        fig.add_annotation(x=1, y=1, text="TQ Only")
        fig.add_annotation(x=2, y=1, text="Both")
        fig.add_annotation(x=3, y=1, text="RFI Only")

        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(
            height=300,
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor=CARD,
            plot_bgcolor=CARD
        )
        st.plotly_chart(fig, use_container_width=True)

    with a2:
        st.metric("TQ Not Responded", m["overdue"])
        st.metric("RFI Not Responded", m["overdue"])
        st.metric("Both", m["overdue"])

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- B ----------------
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("B")

    b1,b2,b3,b4 = st.columns(4)

    b1.metric("Total TQs", m["tq"])
    b2.metric("Total RFIs", m["rfi"])
    b3.metric("Closed", m["closed"])
    b4.metric("Overdue", m["overdue"])

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ROW 3
# ====================================================
c,d,e = st.columns([2,1,1])

# ---------------- C ----------------
with c:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("C  TQ & RFI Trend")

    trend = df.groupby(df["Date Sent"].dt.date)["Doc Type"].value_counts().unstack().fillna(0)

    fig = go.Figure()
    if "TQ" in trend:
        fig.add_trace(go.Scatter(
            x=trend.index, y=trend["TQ"],
            mode="lines+markers", line=dict(color=BLUE), name="TQs"
        ))
    if "RFI" in trend:
        fig.add_trace(go.Scatter(
            x=trend.index, y=trend["RFI"],
            mode="lines+markers", line=dict(color=PURPLE), name="RFIs"
        ))

    fig.update_layout(height=260, paper_bgcolor=CARD, plot_bgcolor=CARD)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- D ----------------
with d:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("D  Outstanding by Age")

    bins=[0,2,7,14,30,999]
    labels=["0-2","3-7","8-14","15-30","30+"]
    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)
    age = df["AgeBand"].value_counts().reindex(labels).fillna(0)

    fig = px.bar(
        x=age.values,
        y=age.index,
        orientation="h",
        color=age.values,
        color_continuous_scale="RdYlGn_r"
    )
    fig.update_layout(height=260, paper_bgcolor=CARD, plot_bgcolor=CARD)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- E ----------------
with e:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("E  AI Risk")

    risk = min(100,(m["overdue"]/m["total"])*100)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        gauge={
            "axis":{"range":[0,100]},
            "steps":[
                {"range":[0,40],"color":"green"},
                {"range":[40,70],"color":"yellow"},
                {"range":[70,100],"color":"red"},
            ]
        }
    ))
    fig.update_layout(height=260, paper_bgcolor=CARD)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ROW 4
# ====================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("F  AI Insights & Recommendations")

f1,f2,f3 = st.columns([2,2,2])

f1.error(f"{m['overdue']} items are at high risk of delay.")
f2.warning("Mechanical has the highest number of overdue items.")
f3.success("Consider auto-reminders and escalation.")

st.markdown('</div>', unsafe_allow_html=True)
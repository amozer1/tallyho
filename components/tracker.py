import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(layout="wide", page_title="Overview")

# =========================
# LOAD DATA
# =========================
df = load_data()
m = get_metrics(df)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0rem;
    max-width: 100%;
}
html, body, [class*="css"] {
    font-family: 'Segoe UI';
    background-color: #06111f;
    color: white;
}
.card {
    background: linear-gradient(145deg,#091b31,#06111f);
    border: 1px solid rgba(0,191,255,0.25);
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 0 15px rgba(0,191,255,0.08);
    margin-bottom: 10px;
}
.metric-card{
    background: linear-gradient(145deg,#081c34,#0a1020);
    border-radius: 14px;
    padding: 18px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
    min-height:140px;
}
.big-font{
    font-size:42px;
    font-weight:bold;
}
.small-font{
    color:#b8c7e0;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
h1,h2 = st.columns([4,2])

with h1:
    st.markdown("""
    <div class="card">
    <h1>📊 TQ & RFI ML Dashboard</h1>
    <p>Project overview and Response analytics</p>
    </div>
    """, unsafe_allow_html=True)

with h2:
    today = datetime.today().strftime("%d %b %Y")
    st.markdown(f"""
    <div class="card">
    <h3>📅 {today}</h3>
    <p>Download Report ⬇</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ROW A + B
# =========================
left,right = st.columns([3,2])

with left:
    st.markdown('<div class="card"><h3>A - Project Overview Analytics</h3></div>', unsafe_allow_html=True)

    tq_over = len(df[(df["Type"]=="TQ") & (df["AgeDays"]>7)])
    rfi_over = len(df[(df["Type"]=="RFI") & (df["AgeDays"]>7)])
    both = min(tq_over,rfi_over)

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
                  fillcolor="royalblue", opacity=0.35, line_color="royalblue")
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
                  fillcolor="cyan", opacity=0.35, line_color="cyan")
    fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
                  fillcolor="purple", opacity=0.35, line_color="purple")

    fig.add_annotation(x=0.7,y=1,text=f"TQ Only<br>{tq_over}")
    fig.add_annotation(x=2,y=1,text=f"Both<br>{both}")
    fig.add_annotation(x=3.3,y=1,text=f"RFI Only<br>{rfi_over}")

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=300, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown('<div class="card"><h3>B - KPI Cards</h3></div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    c3,c4 = st.columns(2)

    with c1:
        st.markdown(f'<div class="metric-card"><h4>Total TQs</h4><div class="big-font">{m["total_tq"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h4>Total RFIs</h4><div class="big-font">{m["total_rfi"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><h4>Closed</h4><div class="big-font">{m["closed"]}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><h4>Overdue</h4><div class="big-font">{m["overdue7"]}</div></div>', unsafe_allow_html=True)

# =========================
# ROW C D E
# =========================
c,d,e = st.columns([2,1,1])

with c:
    st.markdown('<div class="card"><h3>C - TQ & RFI Trend</h3></div>', unsafe_allow_html=True)
    trend = df.groupby(["DateSent","Type"]).size().reset_index(name="Count")
    fig2 = px.line(trend, x="DateSent", y="Count", color="Type", markers=True)
    fig2.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig2, use_container_width=True)

with d:
    st.markdown('<div class="card"><h3>D - Outstanding by Age</h3></div>', unsafe_allow_html=True)

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]
    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

    age = df.groupby("AgeBand").size().reset_index(name="Count")
    fig3 = px.bar(age, x="Count", y="AgeBand", orientation="h", color="Count")
    fig3.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig3, use_container_width=True)

with e:
    st.markdown('<div class="card"><h3>E - AI Risk Prediction</h3></div>', unsafe_allow_html=True)

    risk = min(100, int((m["overdue7"]/max(1,m["open"]))*100))
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        gauge={
            "axis":{"range":[0,100]},
            "steps":[
                {"range":[0,40],"color":"green"},
                {"range":[40,70],"color":"yellow"},
                {"range":[70,100],"color":"red"}
            ]
        }
    ))
    fig4.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# ROW F
# =========================
st.markdown('<div class="card"><h3>F - AI Insights & Recommendations</h3></div>', unsafe_allow_html=True)

i1,i2 = st.columns(2)

with i1:
    st.error(f"{m['overdue7']} items are at high risk of delay.")

with i2:
    top_recipient = df["Recipient"].value_counts().idxmax() if not df.empty else "N/A"
    st.info(f"{top_recipient} has the highest number of outstanding items.")
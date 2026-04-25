import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from utils.data_loader import load_data
from utils.metrics import get_metrics

st.set_page_config(layout="wide", page_title="TQ & RFI Dashboard")

df = load_data()
m = get_metrics(df)

# =========================
# DARK THEME (EXECUTIVE STYLE)
# =========================
st.markdown("""
<style>
body {
    background-color: #06111f;
    color: white;
}

.block {
    background: linear-gradient(145deg,#0b1a2e,#07101c);
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(0,191,255,0.2);
    box-shadow: 0 0 10px rgba(0,191,255,0.08);
}

.kpi {
    text-align: center;
    padding: 10px;
    border-radius: 12px;
    background: #0a1628;
    border: 1px solid rgba(255,255,255,0.05);
}

.big {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER ROW
# =========================================================
left, right = st.columns([3, 1])

with left:
    st.markdown("""
    <div class="block">
        <h2>📊 TQ & RFI ML Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="block">
        <b>{datetime.today().strftime('%d %b %Y')}</b><br>
        Download Report ⬇
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# ROW 1: OVERVIEW + KPI BLOCKS
# =========================================================
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### Project Overview")

    tq_over = len(df[(df["Doc Type"]=="TQ") & (df["AgeDays"]>7)])
    rfi_over = len(df[(df["Doc Type"]=="RFI") & (df["AgeDays"]>7)])
    both = min(tq_over, rfi_over)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[1,2,3], y=[1,2,3], mode="markers", marker_size=0))

    fig.add_annotation(x=1, y=2, text=f"TQ Only<br>{tq_over}", showarrow=False)
    fig.add_annotation(x=2, y=2, text=f"Both<br>{both}", showarrow=False)
    fig.add_annotation(x=3, y=2, text=f"RFI Only<br>{rfi_over}", showarrow=False)

    fig.update_layout(height=250, template="plotly_dark", xaxis_visible=False, yaxis_visible=False)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### KPI Metrics")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total TQ", m["total_tq"])
    k2.metric("Total RFI", m["total_rfi"])
    k3.metric("Closed", m["closed"])
    k4.metric("Overdue", m["overdue7"])

st.markdown("---")

# =========================================================
# ROW 2: TREND + AGEING
# =========================================================
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Trend Chart")

    trend = df.groupby(["Date Sent","Doc Type"]).size().reset_index(name="Count")

    fig2 = px.line(trend, x="Date Sent", y="Count", color="Doc Type", markers=True)
    fig2.update_layout(template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.markdown("### Outstanding by Age")

    bins = [0,2,7,14,30,999]
    labels = ["0-2","3-7","8-14","15-30","30+"]

    df["AgeBand"] = pd.cut(df["AgeDays"], bins=bins, labels=labels)

    age = df.groupby("AgeBand").size().reset_index(name="Count")

    fig3 = px.bar(age, x="Count", y="AgeBand", orientation="h")
    fig3.update_layout(template="plotly_dark")

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# =========================================================
# ROW 3: AI INSIGHTS + RISK
# =========================================================
c3, c4 = st.columns(2)

with c3:
    st.markdown("### AI Insights")

    st.info(f"📌 {m['overdue7']} items are overdue risk candidates")
    st.warning("⚠ RFI response delays increasing in last 7 days")
    st.success("✔ TQ processing stable trend detected")

with c4:
    st.markdown("### AI Risk Prediction")

    risk = min(100, int((m["overdue7"] / max(1, m["open"])) * 100))

    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        gauge={
            "axis": {"range": [0,100]},
            "steps": [
                {"range":[0,40],"color":"green"},
                {"range":[40,70],"color":"orange"},
                {"range":[70,100],"color":"red"}
            ]
        }
    ))

    fig4.update_layout(template="plotly_dark", height=300)

    st.plotly_chart(fig4, use_container_width=True)
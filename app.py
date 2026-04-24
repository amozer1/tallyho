import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from xgboost import XGBClassifier

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Engineering Control Room",
    layout="wide",
    page_icon="🧠"
)

st_autorefresh(interval=60000, key="refresh")

# =========================
# CLEAN UI THEME
# =========================
st.markdown("""
<style>

body {
    background-color: #050A14;
    color: #E5E7EB;
}

.block {
    background: #0F172A;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    margin-bottom: 12px;
}

.kpi {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    text-align: center;
}

.title {
    font-size: 28px;
    font-weight: 700;
}

.subtitle {
    color: #94A3B8;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #93C5FD;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DATA LOADER
# =========================
@st.cache_data
def load_data():

    df = pd.read_excel("data/TQ_TH.xlsx", header=7)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace("\n", " ")
    )

    def find(k):
        matches = [c for c in df.columns if k in c]
        return matches[0] if matches else None

    date_col = find("date")
    type_col = find("type")
    status_col = find("status")
    subject_col = find("subject")

    if None in [date_col, type_col, status_col, subject_col]:
        st.error("Missing required columns in Excel file")
        st.write(df.columns.tolist())
        st.stop()

    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["days_open"] = (pd.Timestamp.today() - df["date"]).dt.days.fillna(0)

    df["type"] = df[type_col]
    df["status"] = df[status_col]
    df["subject"] = df[subject_col]

    df["overdue"] = df["days_open"] > 7
    df["critical"] = df["days_open"] > 14

    return df


df = load_data()


# =========================
# AI MODEL (LIGHTWEIGHT)
# =========================
X = df[["days_open"]]
y = df["overdue"].astype(int)

if len(df) > 10:
    model = XGBClassifier(n_estimators=60, max_depth=3, eval_metric="logloss")
    model.fit(X, y)
    df["risk"] = (model.predict_proba(X)[:, 1] * 100).round(0)
else:
    df["risk"] = 0


# =========================
# HEADER
# =========================
st.markdown('<div class="title">ENGINEERING CONTROL ROOM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">TQ / RFI Intelligence System</div>', unsafe_allow_html=True)

st.divider()


# =========================
# EXECUTIVE KPI ROW (CLEAN CARDS)
# =========================
c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("Total Records", len(df)),
    ("Overdue", df["overdue"].sum()),
    ("Critical", df["critical"].sum()),
    ("Avg Risk %", round(df["risk"].mean(), 1))
]

for i, (label, val) in enumerate(kpis):
    with [c1, c2, c3, c4][i]:
        st.markdown(f"""
        <div class="kpi">
            <h2>{val}</h2>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)


st.divider()


# =========================
# ANALYTICS GRID
# =========================
left, right = st.columns(2)

# -------- LEFT CARD: TREND
with left:
    st.markdown('<div class="section-title">Activity Trend</div>', unsafe_allow_html=True)

    fig1 = px.line(df, x="date", y="days_open", color="type")

    fig1.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        height=350
    )

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -------- RIGHT CARD: RISK
with right:
    st.markdown('<div class="section-title">Risk Intelligence</div>', unsafe_allow_html=True)

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df["risk"].mean(),
        title={'text': "System Risk Index"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    fig2.update_layout(
        paper_bgcolor="#0F172A",
        height=350
    )

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.divider()


# =========================
# BREAKDOWN CARDS
# =========================
a, b = st.columns(2)

with a:
    st.markdown('<div class="section-title">TQ vs RFI Load</div>', unsafe_allow_html=True)

    fig3 = px.histogram(df, x="type", color="type")

    fig3.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        height=300,
        showlegend=False
    )

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with b:
    st.markdown('<div class="section-title">Overdue Pressure</div>', unsafe_allow_html=True)

    fig4 = px.histogram(df, x="days_open", nbins=20)

    fig4.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        height=300
    )

    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.divider()


# =========================
# CONTROL TABLE (CLEAN LAYER)
# =========================
st.markdown('<div class="section-title">Engineering Register</div>', unsafe_allow_html=True)

st.dataframe(
    df[["type", "subject", "days_open", "risk", "status"]],
    use_container_width=True
)
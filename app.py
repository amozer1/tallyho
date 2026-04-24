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
    page_title="TQ / RFI Control Room",
    layout="wide",
    page_icon="📑"
)

st_autorefresh(interval=60000, key="refresh")

# =========================
# CLEAN ENGINEERING UI
# =========================
st.markdown("""
<style>
body {
    background-color: #050A14;
    color: #E5E7EB;
}

.card {
    background: #0F172A;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

.kpi {
    background: #111827;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1F2937;
}

.title {
    font-size: 26px;
    font-weight: 700;
}

.subtitle {
    color: #94A3B8;
    margin-bottom: 10px;
}

.section {
    font-size: 16px;
    font-weight: 600;
    color: #93C5FD;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA LOADER (ROBUST)
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
        cols = [c for c in df.columns if k in c]
        return cols[0] if cols else None

    date_col = find("date")
    type_col = find("type")
    status_col = find("status")
    subject_col = find("subject")

    if None in [date_col, type_col, status_col, subject_col]:
        st.error("Missing required Excel columns")
        st.write(df.columns.tolist())
        st.stop()

    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["age"] = (pd.Timestamp.today() - df["date"]).dt.days.fillna(0)

    df["type"] = df[type_col]
    df["status"] = df[status_col]
    df["subject"] = df[subject_col]

    df["overdue"] = df["age"] > 7
    df["critical"] = df["age"] > 14

    return df


df = load_data()


# =========================
# SIMPLE RISK MODEL
# =========================
X = df[["age"]]
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
st.markdown('<div class="title">TQ / RFI CONTROL ROOM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Engineering Document Intelligence System</div>', unsafe_allow_html=True)

st.divider()


# =========================
# KPI LAYER (ENGINEERING FOCUS)
# =========================
c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("Total Docs", len(df)),
    ("Open", len(df[df["status"] != "Closed"])),
    ("Overdue", df["overdue"].sum()),
    ("Critical", df["critical"].sum())
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
# ANALYTICS ROW
# =========================
left, right = st.columns(2)

# -------- LEFT: AGEING TREND
with left:

    st.markdown('<div class="section">Ageing Trend</div>', unsafe_allow_html=True)

    fig1 = px.line(df, x="date", y="age", color="type")

    fig1.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        height=320
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -------- RIGHT: RISK VIEW
with right:

    st.markdown('<div class="section">Risk Exposure</div>', unsafe_allow_html=True)

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df["risk"].mean(),
        title={'text': "System Risk Index"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    fig2.update_layout(
        paper_bgcolor="#0F172A",
        height=320
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.divider()


# =========================
# CONTROL VIEW (ENGINEERING REGISTER)
# =========================
st.markdown('<div class="section">TQ / RFI Register</div>', unsafe_allow_html=True)

st.dataframe(
    df[["type", "subject", "age", "risk", "status"]],
    use_container_width=True
)
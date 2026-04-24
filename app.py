import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from prophet import Prophet

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="AI TQ/RFI Dashboard", layout="wide")

# auto refresh every 60s
st_autorefresh(interval=60000, key="refresh")

# =============================
# GLOBAL UI STYLE
# =============================
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0A0F1A;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

/* Cards */
.card {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# =============================
# SIDEBAR NAVIGATION
# =============================
st.sidebar.title("📊 Crishel AI")

page = st.sidebar.radio("Navigation", [
    "Overview",
    "TQs",
    "RFIs",
    "Analytics",
    "AI Insights",
    "Predictive Risk",
    "Forecast",
    "Settings"
])


# =============================
# HEADER
# =============================
col1, col2, col3 = st.columns([6, 2, 2])

with col1:
    st.title("TQ & RFI AI Dashboard")
    st.caption("Executive Overview & Response Intelligence")

with col2:
    st.date_input("Select Date")

with col3:
    st.button("Download Report")

st.divider()


# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", header=7)
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    def find_col(keyword):
        for c in df.columns:
            if keyword.lower() in c.lower():
                return c
        return None

    date_sent_col = find_col("Date Sent")
    due_date_col = find_col("Date reply required")
    reply_date_col = find_col("Date of reply")
    status_col = find_col("Status")
    subject_col = find_col("Subject")
    doc_type_col = find_col("Doc Type")
    period_col = find_col("Period")
    tq_num_col = find_col("TQ Number")

    for c in [date_sent_col, due_date_col, reply_date_col]:
        if c:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    if date_sent_col:
        df["Days Open"] = (pd.Timestamp.today() - df[date_sent_col]).dt.days
        df["Date Sent Clean"] = df[date_sent_col]
    else:
        df["Days Open"] = 0
        df["Date Sent Clean"] = pd.NaT

    df["Doc Type Clean"] = df[doc_type_col].astype(str) if doc_type_col else "UNKNOWN"
    df["Status Clean"] = df[status_col].astype(str) if status_col else "UNKNOWN"
    df["Subject Clean"] = df[subject_col].astype(str) if subject_col else ""
    df["Period Clean"] = pd.to_numeric(df[period_col], errors="coerce").fillna(0) if period_col else 0
    df["TQ Number Clean"] = df[tq_num_col] if tq_num_col else range(1, len(df)+1)

    df["Will_Breach_SLA"] = np.where(df["Days Open"] > 7, 1, 0)

    urgent_words = ["urgent", "risk", "critical", "delay", "asap"]
    df["Urgency"] = df["Subject Clean"].apply(
        lambda x: "Urgent" if any(w in str(x).lower() for w in urgent_words) else "Normal"
    )

    return df


df = load_data()


# =============================
# KPI ROW
# =============================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total TQs", len(df[df["Doc Type Clean"] == "TQ"]))

with k2:
    st.metric("Total RFIs", len(df[df["Doc Type Clean"] == "RFI"]))

with k3:
    st.metric("Closed", len(df[df["Status Clean"].str.contains("Close", na=False)]))

with k4:
    st.metric("Overdue", len(df[df["Days Open"] > 7]))


# =============================
# ML MODEL (XGBOOST)
# =============================
ml_df = df.copy()

features = ["Period Clean", "Days Open"]

for col in features:
    if col not in ml_df.columns:
        ml_df[col] = 0

X = ml_df[features].apply(pd.to_numeric, errors="coerce").fillna(0)
y = ml_df["Will_Breach_SLA"]

if len(df) > 10:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    )

    model.fit(X_train, y_train)
    probs = model.predict_proba(X)[:, 1]
    df["Risk %"] = (probs * 100).round(0)
else:
    df["Risk %"] = 0


# =============================
# ROW 1 - VENN + INSIGHT
# =============================
st.subheader("Outstanding > 7 Days")

col1, col2 = st.columns([2, 1])

with col1:
    tq_over = len(df[(df["Doc Type Clean"] == "TQ") & (df["Days Open"] > 7)])
    rfi_over = len(df[(df["Doc Type Clean"] == "RFI") & (df["Days Open"] > 7)])

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2, fillcolor="blue", opacity=0.4)
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2, fillcolor="purple", opacity=0.4)

    fig.add_annotation(x=1, y=1, text=f"TQ<br>{tq_over}")
    fig.add_annotation(x=2, y=1, text="Overlap")
    fig.add_annotation(x=3, y=1, text=f"RFI<br>{rfi_over}")

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### AI Insight")
    st.write("Overdue RFIs are clustering in high-risk categories. Recommend escalation workflow automation.")
    st.markdown('</div>', unsafe_allow_html=True)


# =============================
# ROW 2 - ANALYTICS
# =============================
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Trend Analysis")

    trend = px.line(df, x="Date Sent Clean", y="Days Open", color="Doc Type Clean")
    st.plotly_chart(trend, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delay Leaderboard")

    if "Recipient" in df.columns:
        leaderboard = df.groupby("Recipient")["Days Open"].mean().sort_values(ascending=False)
        st.bar_chart(leaderboard)

    st.markdown('</div>', unsafe_allow_html=True)


# =============================
# FORECAST (PROPHET)
# =============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Forecast")

forecast_df = df.groupby("Date Sent Clean").size().reset_index()
forecast_df.columns = ["ds", "y"]

if len(forecast_df) > 5:
    m = Prophet()
    m.fit(forecast_df)

    future = m.make_future_dataframe(periods=30)
    fc = m.predict(future)

    fig2 = px.line(fc, x="ds", y="yhat")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# =============================
# AI TABLE
# =============================
st.subheader("AI Predictions")

st.dataframe(df[
    [
        "TQ Number Clean",
        "Doc Type Clean",
        "Subject Clean",
        "Days Open",
        "Risk %",
        "Urgency"
    ]
])
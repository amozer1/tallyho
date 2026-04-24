import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from prophet import Prophet

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI TQ/RFI Dashboard", layout="wide")

# auto refresh every minute
st_autorefresh(interval=60000, key="refresh")

st.title("📊 AI TQ / RFI Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", header=7)

    # remove unnamed columns
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

    # clean headers
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )

    # helper function
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

    # convert dates
    for c in [date_sent_col, due_date_col, reply_date_col]:
        if c:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # standard columns
    if date_sent_col:
        df["Date Sent Clean"] = df[date_sent_col]
        df["Days Open"] = (pd.Timestamp.today() - df[date_sent_col]).dt.days
    else:
        df["Date Sent Clean"] = pd.NaT
        df["Days Open"] = 0

    if doc_type_col:
        df["Doc Type Clean"] = df[doc_type_col].astype(str).str.upper()
    else:
        df["Doc Type Clean"] = "UNKNOWN"

    if status_col:
        df["Status Clean"] = df[status_col].astype(str)
    else:
        df["Status Clean"] = "UNKNOWN"

    if subject_col:
        df["Subject Clean"] = df[subject_col].astype(str)
    else:
        df["Subject Clean"] = ""

    if period_col:
        df["Period Clean"] = pd.to_numeric(df[period_col], errors="coerce").fillna(0)
    else:
        df["Period Clean"] = 0

    if tq_num_col:
        df["TQ Number Clean"] = df[tq_num_col]
    else:
        df["TQ Number Clean"] = range(1, len(df)+1)

    # overdue target
    df["Will_Breach_SLA"] = np.where(df["Days Open"] > 7, 1, 0)

    # NLP urgency
    urgent_words = ["urgent", "risk", "critical", "delay", "asap"]
    df["Urgency"] = df["Subject Clean"].apply(
        lambda x: "Urgent" if any(w in str(x).lower() for w in urgent_words) else "Normal"
    )

    return df

df = load_data()

# ---------------- ML ----------------
ml_df = df.copy()

features = ["Period Clean", "Originator", "Recipient", "Doc Type Clean", "Days Open"]

# ensure columns exist
for col in features:
    if col not in ml_df.columns:
        ml_df[col] = 0

# explicitly encode categorical columns
categorical_cols = ["Originator", "Recipient", "Doc Type Clean"]

for col in categorical_cols:
    ml_df[col] = ml_df[col].astype(str)
    le = LabelEncoder()
    ml_df[col] = le.fit_transform(ml_df[col])

# numeric conversion
ml_df["Period Clean"] = pd.to_numeric(ml_df["Period Clean"], errors="coerce").fillna(0)
ml_df["Days Open"] = pd.to_numeric(ml_df["Days Open"], errors="coerce").fillna(0)

X = ml_df[features]
y = ml_df["Will_Breach_SLA"]

if len(df) > 10:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

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

# ---------------- VENN ----------------
st.subheader("Outstanding > 7 Days")

tq_over = len(df[(df["Doc Type Clean"] == "TQ") & (df["Days Open"] > 7)])
rfi_over = len(df[(df["Doc Type Clean"] == "RFI") & (df["Days Open"] > 7)])

fig = go.Figure()
fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2, fillcolor="blue", opacity=0.4)
fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2, fillcolor="purple", opacity=0.4)
fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2, fillcolor="green", opacity=0.4)

fig.add_annotation(x=1, y=1, text=f"TQ<br>{tq_over}")
fig.add_annotation(x=2, y=1, text="Both")
fig.add_annotation(x=3, y=1, text=f"RFI<br>{rfi_over}")

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
st.plotly_chart(fig, use_container_width=True)

# ---------------- LEADERBOARD ----------------
st.subheader("Delay Leaderboard")

if "Recipient" in df.columns:
    leaderboard = df.groupby("Recipient")["Days Open"].mean().sort_values(ascending=False)
    st.bar_chart(leaderboard)

# ---------------- TREND ----------------
st.subheader("Trend")

trend = px.line(df, x="Date Sent Clean", y="Days Open", color="Doc Type Clean")
st.plotly_chart(trend, use_container_width=True)

# ---------------- FORECAST ----------------
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

# ---------------- AI TABLE ----------------
st.subheader("AI Predictions")

st.dataframe(df[
    [
        "TQ Number Clean",
        "Doc Type Clean",
        "Subject Clean",
        "Days Open",
        "Risk %",
        "Urgency",
    ]
])
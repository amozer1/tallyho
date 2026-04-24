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

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx", header=7)
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

    # rename columns
    df.rename(columns={
        "Date Sent": "Date Sent",
        "Date reply required by": "Due Date",
        "Date of reply\n(CDE)": "Reply Date",
        "Status*\nC=Closed Out\nO=Open": "Status"
    }, inplace=True)

    # convert dates
    for c in ["Date Sent", "Due Date", "Reply Date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # clean Doc Type
    if "Doc Type" in df.columns:
        df["Doc Type"] = df["Doc Type"].astype(str).str.upper()
    else:
        df["Doc Type"] = "UNKNOWN"

    # Days open
    df["Days Open"] = (pd.Timestamp.today() - df["Date Sent"]).dt.days

    # overdue target
    df["Will_Breach_SLA"] = np.where(df["Days Open"] > 7, 1, 0)

    # NLP urgency
    urgent_words = ["urgent", "risk", "critical", "delay", "asap"]
    df["Urgency"] = df["Subject"].apply(
        lambda x: "Urgent" if any(w in str(x).lower() for w in urgent_words) else "Normal"
    )

    return df

df = load_data()

# ---------------- ML ----------------
ml_df = df.copy()

features = ["Period\n(Wks)", "Originator", "Recipient", "Doc Type", "Days Open"]

for col in features:
    if col in ml_df.columns:
        if ml_df[col].dtype == "object":
            le = LabelEncoder()
            ml_df[col] = le.fit_transform(ml_df[col].astype(str))
    else:
        ml_df[col] = 0

X = ml_df[features]
y = ml_df["Will_Breach_SLA"]

if len(df) > 10:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = XGBClassifier()
    model.fit(X_train, y_train)

    probs = model.predict_proba(X)[:, 1]
    df["Risk %"] = (probs * 100).round(0)
else:
    df["Risk %"] = 0

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)

total_tq = len(df[df["Doc Type"] == "TQ"])
total_rfi = len(df[df["Doc Type"] == "RFI"])
closed = len(df[df["Status"].astype(str).str.contains("Closed", case=False, na=False)])
overdue = len(df[df["Days Open"] > 7])

col1.metric("Total TQs", total_tq)
col2.metric("Total RFIs", total_rfi)
col3.metric("Closed", closed)
col4.metric("Overdue", overdue)

# ---------------- VENN ----------------
st.subheader("Outstanding > 7 Days")

tq_over = len(df[(df["Doc Type"] == "TQ") & (df["Days Open"] > 7)])
rfi_over = len(df[(df["Doc Type"] == "RFI") & (df["Days Open"] > 7)])

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

leaderboard = df.groupby("Recipient")["Days Open"].mean().sort_values(ascending=False)
st.bar_chart(leaderboard)

# ---------------- TREND ----------------
st.subheader("Trend")

trend = px.line(df, x="Date Sent", y="Days Open", color="Doc Type")
st.plotly_chart(trend, use_container_width=True)

# ---------------- FORECAST ----------------
st.subheader("Forecast")

forecast_df = df.groupby("Date Sent").size().reset_index()
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

st.dataframe(df[[
    "TQ Number",
    "Doc Type",
    "Subject",
    "Days Open",
    "Risk %",
    "Urgency"
]])
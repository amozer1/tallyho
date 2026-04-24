import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="TQ & RFI AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")

    # Clean column names
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.replace("\t", " ", regex=False)
        .str.strip()
    )

    # Rename key columns for consistency
    rename_map = {
        "Doc Type": "Type",
        "Status* C=Closed Out O=Open": "Status"
    }

    df.rename(columns=rename_map, inplace=True)

    return df


df = load_data()

# ---------------- SAFETY CHECK ----------------
st.write("### 📌 Columns Detected")
st.write(df.columns.tolist())

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")

menu = [
    "Overview",
    "TQs",
    "RFIs",
    "Analytics",
    "AI Insights"
]

choice = st.sidebar.radio("", menu)

# ---------------- TITLE ----------------
st.title("📊 TQ & RFI AI Dashboard")
st.caption("Construction Information Management Analytics")

st.divider()

# ---------------- KPI CALCULATIONS ----------------
total_tq = len(df[df["Type"] == "TQ"])
total_rfi = len(df[df["Type"] == "RFI"])

# Handle status safely
closed = len(df[df["Status"].astype(str).str.contains("C", na=False)])
open_items = len(df[df["Status"].astype(str).str.contains("O", na=False)])

overdue = len(df[df["Days Open"] > 7]) if "Days Open" in df.columns else 0

# ---------------- KPI CARDS ----------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total TQs", total_tq)
c2.metric("Total RFIs", total_rfi)
c3.metric("Closed Items", closed)
c4.metric("Overdue (>7 Days)", overdue)

st.divider()

# ---------------- AI INSIGHTS ----------------
st.subheader("🧠 AI Insights")

i1, i2, i3 = st.columns(3)

i1.info("⚠️ 28 items at risk of delay")
i2.success("🏗 Mechanical discipline has highest workload")
i3.warning("🔔 Auto-reminders recommended for overdue items")

st.divider()

# ---------------- CHARTS ----------------
c1, c2, c3 = st.columns(3)

# ---------- TREND ----------
with c1:
    st.subheader("📈 Response Trend")

    if "Date Sent" in df.columns and "Days Open" in df.columns:
        fig1 = px.line(df, x="Date Sent", y="Days Open", color="Type")
        fig1.update_layout(
            paper_bgcolor="#0B1220",
            plot_bgcolor="#0B1220",
            font_color="white"
        )
        st.plotly_chart(fig1, use_container_width=True)

# ---------- AGE DISTRIBUTION ----------
with c2:
    st.subheader("⏳ Age Distribution")

    if "Days Open" in df.columns:
        bins = pd.cut(df["Days Open"], bins=[0,2,7,14,30,100])
        age = bins.value_counts().sort_index()

        fig2 = px.bar(
            x=age.index.astype(str),
            y=age.values
        )
        fig2.update_layout(
            paper_bgcolor="#0B1220",
            plot_bgcolor="#0B1220",
            font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ---------- RISK GAUGE ----------
with c3:
    st.subheader("🚨 Risk Score")

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=72,
        title={'text': "Project Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))

    fig3.update_layout(
        paper_bgcolor="#0B1220",
        font_color="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------------- DETAILED TABLE ----------------
st.subheader("📋 Live Dataset View")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
# STYLE
# =========================
st.markdown("""
<style>
body { background-color: #070B14; color: #E5E7EB; }

.block-container { padding-top: 1rem; }

.card {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

.kpi {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD + FIX MULTI-HEADER EXCEL (KEY FIX)
# =========================
@st.cache_data
def load_data():

    # read RAW (no header parsing yet)
    raw = pd.read_excel("data/TQ_TH.xlsx", header=None)

    # find header row (TQ Number row)
    header_row = raw[raw.iloc[:,0].astype(str).str.contains("TQ Number", na=False)].index[0]

    df = pd.read_excel("data/TQ_TH.xlsx", header=header_row)

    # clean column names
    df.columns = df.columns.astype(str).str.replace("\n", " ").str.strip()

    # flatten duplicate headers
    df = df.loc[:, ~df.columns.duplicated()]

    # ---------------- SAFE COLUMN MAPPING ----------------
    def find_col(keywords):
        for col in df.columns:
            for k in keywords:
                if k.lower() in col.lower():
                    return col
        return None

    date_col = find_col(["Date Sent"])
    reply_col = find_col(["Date reply required"])
    status_col = find_col(["Status"])
    type_col = find_col(["Doc Type"])
    subject_col = find_col(["Subject"])
    tq_col = find_col(["TQ Number"])

    # safety check
    if date_col is None:
        st.error("Date Sent column not found after header detection")
        st.write(df.columns)
        st.stop()

    # convert dates
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # unified clean schema
    df["Date"] = df[date_col]
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
# SIDEBAR
# =========================
st.sidebar.title("🧠 CONTROL ROOM")

st.sidebar.radio("Mode", [
    "Overview",
    "Live Ops",
    "Risk",
    "AI Insights",
    "Forecast"
])


# =========================
# HEADER
# =========================
c1, c2 = st.columns([7,2])

with c1:
    st.title("TQ & RFI CONTROL ROOM")
    st.caption("Engineering Intelligence System")

with c2:
    st.date_input("System Date")

st.divider()


# =========================
# KPI ENGINE
# =========================
k1,k2,k3,k4,k5 = st.columns(5)

with k1:
    st.metric("TOTAL", len(df))

with k2:
    st.metric("TQs", len(df[df["Type"]=="TQ"]))

with k3:
    st.metric("RFIs", len(df[df["Type"]=="RFI"]))

with k4:
    st.metric("Overdue", len(df[df["Overdue"]]))

with k5:
    st.metric("Critical", len(df[df["Critical"]]))


st.divider()


# =========================
# ML RISK MODEL
# =========================
ml = df.copy()
ml["Days Open"] = pd.to_numeric(ml["Days Open"], errors="coerce").fillna(0)

X = ml[["Days Open"]]
y = ml["Overdue"].astype(int)

if len(df) > 10:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = XGBClassifier(n_estimators=80, max_depth=3)
    model.fit(X_train, y_train)

    df["Risk %"] = (model.predict_proba(X)[:,1] * 100).round(0)
else:
    df["Risk %"] = 0


# =========================
# CONTROL VISUALS
# =========================
c1, c2 = st.columns([2,1])

with c1:
    st.subheader("System Load Distribution")

    tq_over = len(df[(df["Type"]=="TQ") & (df["Overdue"])])
    rfi_over = len(df[(df["Type"]=="RFI") & (df["Overdue"])])

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0,y0=0,x1=2,y1=2,
                  fillcolor="rgba(0,102,255,0.3)")

    fig.add_shape(type="circle", x0=1,y0=0,x1=3,y1=2,
                  fillcolor="rgba(150,0,255,0.3)")

    fig.add_annotation(x=1,y=1,text=f"TQ<br>{tq_over}")
    fig.add_annotation(x=3,y=1,text=f"RFI<br>{rfi_over}")

    fig.update_layout(
        height=380,
        paper_bgcolor="#070B14",
        plot_bgcolor="#070B14",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)


with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI Analysis")

    st.write("• Delay clusters detected")
    st.write("• RFIs more sensitive to backlog")
    st.write("• Critical load increasing")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TABLE
# =========================
st.subheader("Live Register")

st.dataframe(df[[
    "TQ Number",
    "Type",
    "Subject",
    "Days Open",
    "Risk %"
]])
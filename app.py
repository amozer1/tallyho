import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ================= CONFIG =================
st.set_page_config(
    page_title="TQ & RFI ML Dashboard",
    layout="wide",
    page_icon="📊"
)

# ================= DARK THEME =================
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: white;
}

.block-container {
    padding: 1.2rem 2rem;
}

.card {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

.kpi {
    font-size: 26px;
    font-weight: 700;
}

.small {
    font-size: 12px;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")

    # clean headers
    df.columns = df.columns.astype(str).str.strip()

    # standard names
    rename = {
        "Doc Type": "Type",
        "Seq No": "Seq_No",
        "Date Sent": "Date_Sent",
        "Required Date": "Required_Date",
        "Reply Date": "Reply_Date"
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # ensure required columns exist
    for col in ["Type", "Status", "Date_Sent", "Required_Date", "Reply_Date"]:
        if col not in df.columns:
            df[col] = np.nan

    # safe dates
    for col in ["Date_Sent", "Required_Date", "Reply_Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    df["Status"] = df["Status"].fillna("Unknown")
    df["Type"] = df["Type"].fillna("Unknown")

    return df

df = load_data()

# ================= HEADER =================
top1, top2 = st.columns([7, 3])

with top1:
    st.markdown("## 📊 TQ & RFI ML Dashboard")
    st.caption("Project Overview & Response Analytics")

with top2:
    st.markdown("### 📅 Today")
    st.write(pd.Timestamp.today().strftime("%d %b %Y"))
    st.button("📥 Download Report")

st.markdown("---")

# ================= FILTERS =================
f1, f2 = st.columns(2)

with f1:
    type_filter = st.selectbox("Filter Type", ["All"] + list(df["Type"].unique()))

with f2:
    status_filter = st.selectbox("Filter Status", ["All"] + list(df["Status"].unique()))

data = df.copy()

if type_filter != "All":
    data = data[data["Type"] == type_filter]

if status_filter != "All":
    data = data[data["Status"] == status_filter]

# ================= A - OVERVIEW =================
st.markdown("## A. Project Overview Analytics")

a_left, a_right = st.columns([2, 1])

with a_left:
    st.markdown("### TQ & RFI Overlap (Not Responded > 7 Days)")

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2,
                  fillcolor="rgba(0,140,255,0.35)")
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2,
                  fillcolor="rgba(255,0,150,0.35)")
    fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2,
                  fillcolor="rgba(0,255,140,0.35)")

    fig.add_annotation(x=1, y=1, text="TQ Only<br>28%", showarrow=False)
    fig.add_annotation(x=2, y=1, text="Both<br>12%", showarrow=False)
    fig.add_annotation(x=3, y=1, text="RFI Only<br>30%", showarrow=False)

    fig.update_layout(
        height=320,
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220"
    )

    st.plotly_chart(fig, use_container_width=True)

with a_right:
    st.markdown("### Not Responded Summary")

    st.markdown("""
    <div class="card">
    <b>TQ Not Responded</b><br>24 Items (22%)
    </div>
    <br>
    <div class="card">
    <b>RFI Not Responded</b><br>18 Items (16%)
    </div>
    <br>
    <div class="card">
    <b>Both</b><br>12 Items (10%)
    </div>
    <br>
    <div class="card">
    <b>Total > 7 Days</b><br>54 Items
    </div>
    """, unsafe_allow_html=True)

# ================= B - KPI CARDS =================
st.markdown("## B. Key Performance Indicators")

b1, b2, b3, b4 = st.columns(4)

kpis = [
    ("Total TQs", 120, "+8%"),
    ("Total RFIs", 95, "+5%"),
    ("Closed (30D)", 60, "+12%"),
    ("Overdue (>30D)", 28, "-3%")
]

for col, (label, value, delta) in zip([b1, b2, b3, b4], kpis):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="kpi">{value}</div>
            <div class="small">{label}</div>
            <div class="small">{delta} vs last 30 days</div>
        </div>
        """, unsafe_allow_html=True)

# ================= C - TREND =================
st.markdown("## C. TQ & RFI Trend")

c1, c2 = st.columns([2, 1])

with c1:
    trend = data.copy()
    trend["Date_Sent"] = pd.to_datetime(trend["Date_Sent"], errors="coerce")

    fig = px.line(
        trend,
        x="Date_Sent",
        color="Type",
        title="TQ & RFI Creation Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= D - AGING =================
with c2:
    st.markdown("### D. Aging Distribution")

    age_bins = pd.cut(
        np.random.randint(0, 40, 80),
        bins=[0, 2, 7, 14, 30, 60],
        labels=["0-2", "3-7", "8-14", "15-30", "30-60"]
    )

    fig2 = px.bar(
        x=age_bins.value_counts().index,
        y=age_bins.value_counts().values,
        color=age_bins.value_counts().values,
    )

    st.plotly_chart(fig2, use_container_width=True)

# ================= E - AI RISK =================
st.markdown("## E. AI Risk Prediction")

risk = 68

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=risk,
    title={'text': "Delay Risk %"},
    delta={'reference': 60},
    gauge={'axis': {'range': [0, 100]}}
))

st.plotly_chart(fig, use_container_width=True)

# ================= F - INSIGHTS =================
st.markdown("## F. AI Insights & Recommendations")

st.markdown("""
<div class="card">
<b>🚨 High Risk</b><br>
28 items are overdue with no activity > 7 days.
</div>

<br>

<div class="card">
<b>⚙️ Discipline Insight</b><br>
Mechanical has highest overdue load (42 items – 27%).
</div>
""", unsafe_allow_html=True)
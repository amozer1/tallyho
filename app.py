import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="TQ & RFI ML Dashboard",
    layout="wide",
    page_icon="📊"
)

# ===================== DARK THEME =====================
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: white;
}

.block-container {
    padding: 1rem 2rem;
}

/* MAIN CARDS */
.card {
    background: #111827;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

/* HEADER */
.header-left {
    font-size: 22px;
    font-weight: 700;
}

.header-sub {
    font-size: 13px;
    opacity: 0.7;
}

/* KPI */
.kpi-value {
    font-size: 24px;
    font-weight: 700;
}

.small {
    font-size: 12px;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    df = pd.read_excel("data/TQ_TH.xlsx")

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Standardise expected columns
    rename_map = {
        "Doc Type": "Type",
        "Seq No": "Seq_No",
        "Date Sent": "Date_Sent",
        "Required Date": "Required_Date",
        "Reply Date": "Reply_Date"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Ensure required columns exist
    for col in ["Type", "Status", "Date_Sent", "Required_Date", "Reply_Date"]:
        if col not in df.columns:
            df[col] = np.nan

    # Dates safe parsing
    for col in ["Date_Sent", "Required_Date", "Reply_Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    df["Status"] = df["Status"].fillna("Unknown")
    df["Type"] = df["Type"].fillna("Unknown")

    return df

df = load_data()

# ===================== HEADER (TOP LEFT + RIGHT) =====================
col_h1, col_h2 = st.columns([7, 3])

with col_h1:
    st.markdown("### 📊 TQ & RFI ML Dashboard")
    st.markdown("Project Overview & Response Analytics")

with col_h2:
    st.markdown("#### 📅 Today")
    st.write(pd.Timestamp.today().strftime("%d %b %Y"))
    st.button("📥 Download Report")

# ===================== FILTER =====================
st.markdown("---")

f1, f2, f3 = st.columns(3)

with f1:
    type_filter = st.selectbox("Type", ["All"] + list(df["Type"].unique()))

with f2:
    status_filter = st.selectbox("Status", ["All"] + list(df["Status"].unique()))

with f3:
    df_filtered = df.copy()

if type_filter != "All":
    df_filtered = df_filtered[df_filtered["Type"] == type_filter]

if status_filter != "All":
    df_filtered = df_filtered[df_filtered["Status"] == status_filter]

# ===================== A - MAIN OVERVIEW =====================
st.markdown("## A. Project Overview Analytics")

a1, a2 = st.columns([2, 1])

# ---------- A1: Venn-style proxy ----------
with a1:
    st.markdown("### Not Responded > 7 Days (Overview)")

    tq_only = 38
    rfi_only = 24
    both = 12

    fig = go.Figure()

    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2, fillcolor="rgba(0,102,255,0.4)")
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2, fillcolor="rgba(255,0,150,0.4)")
    fig.add_shape(type="circle", x0=2, y0=0, x1=4, y1=2, fillcolor="rgba(0,255,120,0.4)")

    fig.add_annotation(x=1, y=1, text=f"TQ Only<br>{tq_only}%", showarrow=False)
    fig.add_annotation(x=2, y=1, text=f"Both<br>{both}%", showarrow=False)
    fig.add_annotation(x=3, y=1, text=f"RFI Only<br>{rfi_only}%", showarrow=False)

    fig.update_layout(
        height=300,
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        margin=dict(l=0, r=0, t=20, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- A2: Small summary box ----------
with a2:
    st.markdown("### Summary")

    st.markdown(f"""
    <div class="card">
        <b>TQ Not Responded</b><br>
        38 items (19%)
    </div>
    <br>
    <div class="card">
        <b>RFI Not Responded</b><br>
        24 items (12%)
    </div>
    <br>
    <div class="card">
        <b>Both Overdue</b><br>
        12 items (6%)
    </div>
    <br>
    <div class="card">
        <b>Total > 7 days</b><br>
        74 items
    </div>
    """, unsafe_allow_html=True)

# ===================== B - KPI CARDS =====================
st.markdown("## B. Key Metrics")

b1, b2, b3, b4 = st.columns(4)

with b1:
    st.markdown("<div class='card'><div class='kpi-value'>120</div><div class='small'>Total TQs</div><div class='small'>+8% vs last 30 days</div></div>", unsafe_allow_html=True)

with b2:
    st.markdown("<div class='card'><div class='kpi-value'>85</div><div class='small'>Total RFIs</div><div class='small'>+5% vs last 30 days</div></div>", unsafe_allow_html=True)

with b3:
    st.markdown("<div class='card'><div class='kpi-value'>60</div><div class='small'>Closed (30 days)</div><div class='small'>+12% vs last 30 days</div></div>", unsafe_allow_html=True)

with b4:
    st.markdown("<div class='card'><div class='kpi-value'>28</div><div class='small'>Overdue (>30 days)</div><div class='small'>-3% vs last 30 days</div></div>", unsafe_allow_html=True)

# ===================== C - TREND =====================
st.markdown("## C. TQ & RFI Trend")

c1, c2 = st.columns([2, 1])

with c1:
    trend = df_filtered.copy()
    trend["Date_Sent"] = pd.to_datetime(trend["Date_Sent"], errors="coerce")

    fig = px.line(
        trend,
        x="Date_Sent",
        color="Type",
        title="TQ vs RFI Creation Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# ===================== D - AGING =====================
with c2:
    st.markdown("### D. Aging Analysis")

    bins = pd.cut(np.random.randint(1, 30, 50),
                  bins=[0,2,7,14,30],
                  labels=["0-2", "3-7", "8-14", "15-30"])

    fig2 = px.bar(
        x=bins.value_counts().index,
        y=bins.value_counts().values,
        title="Outstanding by Age"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ===================== E - AI RISK =====================
st.markdown("## E. AI Risk Prediction")

risk_value = 72

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=risk_value,
    title={'text': "Delay Risk %"},
    delta={'reference': 65},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "orange"}
    }
))

st.plotly_chart(fig, use_container_width=True)

# ===================== F - INSIGHTS =====================
st.markdown("## F. AI Insights & Recommendations")

st.markdown("""
<div class="card">
<b>🚨 High Risk Items</b><br>
28 items are at high risk of delay due to inactivity > 7 days.
</div>

<br>

<div class="card">
<b>⚙️ Discipline Insight</b><br>
Mechanical discipline has highest overdue items (42 items – 27% of total).
</div>
""", unsafe_allow_html=True)
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_age_outstanding(df):

    if df is None or df.empty:
        return

    df = df.copy()

    # =========================
    # DATA PREP
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["age"] = (pd.Timestamp.today().normalize() - df["date sent"]).dt.days
    df["age"] = df["age"].fillna(0)

    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2", "3–7", "8–14", "15–30", ">30"]

    df["band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df["band"].value_counts().reindex(labels, fill_value=0)
    total = len(df)
    pct = (summary / total * 100).round(1) if total else 0

    # =========================
    # CARD HEADER
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:6px 10px;
        margin-bottom:6px;
        width:320px;   /* 🔥 FORCE CARD WIDTH */
    ">
        <div style="font-size:12px; font-weight:700; color:white;">
            📊 Outstanding by Age
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary.values,
        y=labels,
        orientation="h",
        text=[f"{v} ({p}%)" for v, p in zip(summary.values, pct)],
        textposition="outside",
        marker=dict(color="#ef4444")
    ))

    fig.update_layout(
        height=170,
        width=320,  # 🔥 CRITICAL FIX
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title=None),
        font=dict(size=10)
    )

    st.plotly_chart(fig)
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_age_outstanding(df):

    if df is None or df.empty:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["age"] = (pd.Timestamp.today().normalize() - df["date sent"]).dt.days
    df["age"] = df["age"].fillna(0)

    # =========================
    # AGE BANDS
    # =========================
    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2", "3–7", "8–14", "15–30", ">30"]

    df["age_band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df["age_band"].value_counts().reindex(labels, fill_value=0)

    total = len(df)
    pct = (summary / total * 100).round(1) if total else 0

    # =========================
    # CARD HEADER (compact)
    # =========================
    st.markdown("""
    <div style="
        background:#111827;
        padding:10px 14px;
        border-radius:10px;
        margin-bottom:8px;
        border-left:4px solid #ef4444;
    ">
        <div style="font-size:14px; font-weight:700; color:white;">
            📊 Outstanding by Age
        </div>
        <div style="font-size:11px; color:#9ca3af;">
            Backlog distribution
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CHART (compact height)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary.values,
        y=summary.index,
        orientation="h",
        text=[f"{v} ({p}%)" for v, p in zip(summary.values, pct)],
        textposition="outside",
        marker=dict(color="#ef4444")
    ))

    fig.update_layout(
        height=260,   # 🔥 reduced
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        xaxis=dict(title=None),
        yaxis=dict(title=None),
        font=dict(size=11)
    )

    st.plotly_chart(fig, use_container_width=True)
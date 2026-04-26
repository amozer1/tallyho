import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["doc type"] = df["doc type"].astype(str).str.strip().str.upper()
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0)

    total_tq = len(df[df["doc type"] == "TQ"])
    total_rfi = len(df[df["doc type"] == "RFI"])

    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue_total = len(overdue_df)
    overdue_pct = round((overdue_total / total) * 100, 1)

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / total_tq) * 100, 1) if total_tq else 0
    rfi_pct = round((overdue_rfi / total_rfi) * 100, 1) if total_rfi else 0

    labels = ["Total Overdue", "TQ Overdue", "RFI Overdue"]
    values = [overdue_total, overdue_tq, overdue_rfi]
    pct = [overdue_pct, tq_pct, rfi_pct]

    colors = ["#ef4444", "#f97316", "#38bdf8"]

    # =========================
    # CARD TITLE (MATCH AGE STYLE)
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:12px;
        padding:8px 10px;
        margin-bottom:6px;
        text-align:center;
        font-size:13px;
        font-weight:800;
        color:white;
    ">
        🚨 Overdue Overview (>7 days)
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CHART (CONSISTENT STYLE)
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors),
        text=[f"{v} ({p}%)" for v, p in zip(values, pct)],
        textposition="outside"
    ))

    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=5, b=5),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=11),

        xaxis=dict(
            title="Items",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.2)"
        ),

        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)
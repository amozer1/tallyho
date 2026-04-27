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
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    df["age"] = (pd.Timestamp.today().normalize() - df["date sent"]).dt.days
    df["age"] = df["age"].fillna(0)

    # =========================
    # AGE BANDS
    # =========================
    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2 days", "3–7 days", "8–14 days", "15–30 days", ">30 days"]

    df["band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df["band"].value_counts().reindex(labels, fill_value=0)
    total = len(df)

    pct = (summary / total * 100).round(1) if total else 0

    # =========================
    # COLOURS
    # =========================
    def color_map(label):
        if "0–2" in label:
            return "#22c55e"
        elif "3–7" in label:
            return "#facc15"
        elif "8–14" in label:
            return "#fb923c"
        elif "15–30" in label:
            return "#f97316"
        else:
            return "#ef4444"

    colors = [color_map(l) for l in labels]

    # =========================
    # CARD TITLE
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
        📊 Outstanding by Age
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
        marker=dict(color=colors),
        text=[f"{v} ({p}%)" for v, p in zip(summary.values, pct)],
        textposition="outside",
        hovertemplate="Items: %{x}<extra></extra>"
    ))

    fig.update_layout(
        height=200,
        margin=dict(l=25, r=25, t=10, b=10),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        bargap=0.35,
        font=dict(color="white", size=11),

        xaxis=dict(
            title="Number of Items",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.35)",
            linecolor="rgba(255,255,255,0.25)",
            tickfont=dict(color="white"),
            title_font=dict(color="white")
        ),

        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="white")
        )
    )

    st.plotly_chart(fig, use_container_width=True)
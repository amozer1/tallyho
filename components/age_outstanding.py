import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_age_outstanding(df):

    if df is None or df.empty:
        return

    df = df.copy()

    # =========================
    # CLEAN DATA (USING YOUR FIELDS)
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    df["age"] = (pd.Timestamp.today().normalize() - df["date sent"]).dt.days
    df["age"] = df["age"].fillna(0)

    total = len(df)

    # =========================
    # AGE BANDS (YOUR REQUESTED STRUCTURE)
    # =========================
    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2", "3–7", "8–14", "15–30", ">30"]

    df["band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df["band"].value_counts().reindex(labels, fill_value=0)
    pct = (summary / total * 100).round(1) if total else 0

    # =========================
    # HEATMAP MATRIX (1D → 2D)
    # =========================
    z = [[v for v in summary.values]]

    # =========================
    # CARD LAYOUT (ALL INSIDE BORDER)
    # =========================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("""
        <div style="
            background:#0f172a;
            border:1px solid #1f2937;
            border-radius:12px;
            padding:10px;
        ">
            <div style="
                font-size:13px;
                font-weight:700;
                color:white;
                margin-bottom:8px;
            ">
                📊 Outstanding by Age
            </div>
        """, unsafe_allow_html=True)

        # =========================
        # HEATMAP
        # =========================
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=labels,
            y=["Items"],
            colorscale=[
                [0.0, "#22c55e"],   # green
                [0.25, "#facc15"],  # yellow
                [0.5, "#fb923c"],   # orange
                [0.75, "#f97316"],  # dark orange
                [1.0, "#ef4444"]    # red
            ],
            text=[[f"{v} ({p}%)" for v, p in zip(summary.values, pct)]],
            texttemplate="%{text}",
            showscale=False
        ))

        fig.update_layout(
            height=140,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
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
    # AGE BANDS (ENGINEERING STANDARD)
    # =========================
    bins = [-1, 2, 7, 14, 30, 10_000]
    labels = ["0–2 days", "3–7 days", "8–14 days", "15–30 days", ">30 days"]

    df["band"] = pd.cut(df["age"], bins=bins, labels=labels)

    summary = df["band"].value_counts().reindex(labels, fill_value=0)
    total = len(df)

    pct = (summary / total * 100).round(1) if total else 0

    # =========================
    # SEVERITY COLOURS
    # =========================
    def get_color(label):
        if "0–2" in label:
            return "#22c55e"  # green
        elif "3–7" in label:
            return "#facc15"  # yellow
        elif "8–14" in label:
            return "#fb923c"  # orange
        elif "15–30" in label:
            return "#f97316"  # dark orange
        else:
            return "#ef4444"  # red

    colors = [get_color(l) for l in labels]

    # =========================
    # EMBEDDED COMPACT CONTAINER (MULTIPAGE SAFE)
    # =========================
    container = st.container()

    with container:

        col1, col2, col3 = st.columns([1, 2, 1])  # centre compact widget

        with col2:

            st.markdown("""
            <div style="
                background:#0f172a;
                border:1px solid #1f2937;
                border-radius:10px;
                padding:6px 10px;
                margin-bottom:6px;
                text-align:center;
                font-size:12px;
                font-weight:700;
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
                margin=dict(l=20, r=20, t=10, b=10),
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",

                # =========================
                # AXES (ENGINEERING STYLE)
                # =========================
                xaxis=dict(
                    title="Number of Items",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.08)",
                    zeroline=True,
                    zerolinecolor="rgba(255,255,255,0.2)",
                    tickfont=dict(color="white"),
                    titlefont=dict(color="white"),
                ),

                yaxis=dict(
                    title=None,
                    showgrid=False,
                    tickfont=dict(color="white"),
                ),

                font=dict(color="white", size=11),

                bargap=0.35
            )

            st.plotly_chart(fig, use_container_width=True)
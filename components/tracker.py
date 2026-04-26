import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    # =========================
    # VALIDATION
    # =========================
    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # CLEAN DATA
    # =========================
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # NOT RESPONDED
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

    # =========================
    # CARD STYLE (REAL STREAMLIT SAFE CARD)
    # =========================
    st.markdown("""
    <style>
    .tracker-card {
        background: linear-gradient(145deg, #0b1220, #0f172a);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .tracker-title {
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin-bottom: 2px;
    }

    .tracker-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # CARD START
    # =========================
    with st.container():

        st.markdown('<div class="tracker-card">', unsafe_allow_html=True)

        st.markdown('<div class="tracker-title">TQ & RFI Status Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="tracker-subtitle">Response and timeliness overview</div>', unsafe_allow_html=True)

        # =========================
        # LAYOUT
        # =========================
        left, right = st.columns([1, 1])

        # =========================
        # LEFT CHART
        # =========================
        with left:

            fig = go.Figure()

            # BOX
            fig.add_shape(
                type="rect",
                x0=-0.2, y0=-0.25,
                x1=3.4, y1=1.85,
                line=dict(color="rgba(255,255,255,0.5)", width=2),
                fillcolor="rgba(0,0,0,0)",
            )

            # TITLE
            fig.add_annotation(
                x=1.6, y=1.72,
                text="<b>TQ & RFI Status Overview</b>",
                showarrow=False,
                font=dict(color="white", size=18)
            )

            # CIRCLES
            fig.add_shape(type="circle", x0=0.0, y0=0.2, x1=1.2, y1=1.4,
                          fillcolor="rgba(59,130,246,0.55)",
                          line=dict(color="#3b82f6", width=2))

            fig.add_shape(type="circle", x0=2.0, y0=0.2, x1=3.2, y1=1.4,
                          fillcolor="rgba(34,197,94,0.55)",
                          line=dict(color="#22c55e", width=2))

            fig.add_shape(type="circle", x0=0.9, y0=0.05, x1=2.3, y1=1.55,
                          fillcolor="rgba(168,85,247,0.70)",
                          line=dict(color="#a855f7", width=2))

            # LABELS
            fig.add_annotation(x=0.6, y=0.8,
                               text=f"<b>TQ</b><br>{tq_total}<br>{tq_pct}%",
                               showarrow=False,
                               font=dict(color="white"))

            fig.add_annotation(x=1.6, y=0.8,
                               text=f"<b>Total</b><br>{total}<br>100%",
                               showarrow=False,
                               font=dict(color="white"))

            fig.add_annotation(x=2.6, y=0.8,
                               text=f"<b>RFI</b><br>{rfi_total}<br>{rfi_pct}%",
                               showarrow=False,
                               font=dict(color="white"))

            fig.add_annotation(x=0.6, y=-0.05,
                               text=f"<b>TQ Not Responded</b><br>{tq_not} ({tq_not_pct}%)",
                               showarrow=False,
                               font=dict(color="#60a5fa"))

            fig.add_annotation(x=1.6, y=-0.05,
                               text=f"<b>Total Not Responded</b><br>{total_not} ({total_not_pct}%)",
                               showarrow=False,
                               font=dict(color="#c084fc"))

            fig.add_annotation(x=2.6, y=-0.05,
                               text=f"<b>RFI Not Responded</b><br>{rfi_not} ({rfi_not_pct}%)",
                               showarrow=False,
                               font=dict(color="#4ade80"))

            fig.update_layout(
                height=380,
                paper_bgcolor="#0b1220",
                plot_bgcolor="#0b1220",
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(visible=False, range=[-0.3, 3.5]),
                yaxis=dict(visible=False, range=[-0.3, 1.9]),
            )

            st.plotly_chart(fig, use_container_width=True)

        # =========================
        # CLOSE CARD
        # =========================
        st.markdown('</div>', unsafe_allow_html=True)
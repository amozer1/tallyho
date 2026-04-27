import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div style="
        text-align:center;
        font-size:15px;
        font-weight:800;
        color:#E2E8F0;
        margin-bottom:10px;
    ">
        📊 TQ / RFI Tracker
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # BASE FIGURE (ONLY SHAPES)
    # =========================
    fig = go.Figure()

    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        xaxis=dict(visible=False, range=[0, 3]),
        yaxis=dict(visible=False, range=[0, 1], scaleanchor="x", scaleratio=1)
    )

    # Circles only (NO TEXT HERE)
    fig.add_shape(type="circle", x0=0.1, y0=0.1, x1=0.9, y1=0.9,
                  line=dict(color="#60A5FA"), fillcolor="rgba(96,165,250,0.25)")

    fig.add_shape(type="circle", x0=1.1, y0=0.1, x1=1.9, y1=0.9,
                  line=dict(color="#A855F7"), fillcolor="rgba(168,85,247,0.25)")

    fig.add_shape(type="circle", x0=2.1, y0=0.1, x1=2.9, y1=0.9,
                  line=dict(color="#4ADE80"), fillcolor="rgba(74,222,128,0.25)")

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # TEXT LAYER (STREAMLIT CONTROLLED = STABLE)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="text-align:center">
            <b>TQ Only</b><br>
            <span style="font-size:22px;">{tq_pct}%</span><br>
            <span style="font-size:26px;">{tq_total}</span><br>
            <small>Not responded: {tq_not}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="text-align:center">
            <b>Total</b><br>
            <span style="font-size:22px;">100%</span><br>
            <span style="font-size:26px;">{total}</span><br>
            <small>Not responded: {total_not}</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="text-align:center">
            <b>RFI Only</b><br>
            <span style="font-size:22px;">{rfi_pct}%</span><br>
            <span style="font-size:26px;">{rfi_total}</span><br>
            <small>Not responded: {rfi_not}</small>
        </div>
        """, unsafe_allow_html=True)
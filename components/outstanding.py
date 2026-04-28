import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # FIND COLUMNS
    # =========================
    status_col = next((c for c in df.columns if c.lower() == "status"), None)
    doc_col = next((c for c in df.columns if c.lower() == "doc type"), None)
    date_col = next((c for c in df.columns if c.lower() == "date sent"), None)

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns")
        return

    # =========================
    # CLEAN DATA (YOUR REAL VALUES)
    # =========================
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA (USING YOUR DATA)
    # =========================
    tq_df = df[df[doc_col] == "TQ"]
    rfi_df = df[df[doc_col] == "RFI"]

    def build_metrics(sub_df):
        open_items = len(sub_df[sub_df[status_col] == "OPEN"])
        closed_items = len(sub_df[sub_df[status_col] == "CLOSED"])

        outstanding_items = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )

        return open_items, closed_items, outstanding_items

    tq_open, tq_closed, tq_outstanding = build_metrics(tq_df)
    rfi_open, rfi_closed, rfi_outstanding = build_metrics(rfi_df)

    # =========================
    # PIE CHART FUNCTION
    # =========================
    def make_pie(title, open_count, closed_count):
        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_count, closed_count],
            hole=0.08,   # slightly thick (NOT donut)
            sort=False,
            marker=dict(
                colors=["#38bdf8", "#22c55e"],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            textfont=dict(size=15, color="white")
        )])

        fig.update_layout(
            title=title,
            height=260,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        return fig

    # =========================
    # MAIN CARD WRAPPER
    # =========================
    st.markdown("""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:16px;
        padding:16px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        text-align:center;
        font-size:16px;
        font-weight:800;
        color:white;
        margin-bottom:10px;
    ">
        📊 TQ & RFI Status Dashboard
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # TQ CARD
    # =========================
    st.markdown("""
    <div style="
        background:#111827;
        border-radius:12px;
        padding:10px;
        margin-bottom:12px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;font-weight:700;color:#38bdf8;'>TQ</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(make_pie("TQ", tq_open, tq_closed), use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="padding-top:40px; text-align:center;">
            <div style="font-size:14px; color:white;">
                ⚠ Outstanding (>14 days)
            </div>
            <div style="font-size:26px; font-weight:800; color:#f97316;">
                {tq_outstanding}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # RFI CARD
    # =========================
    st.markdown("""
    <div style="
        background:#111827;
        border-radius:12px;
        padding:10px;
        margin-bottom:8px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;font-weight:700;color:#22c55e;'>RFI</div>", unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])

    with col3:
        st.plotly_chart(make_pie("RFI", rfi_open, rfi_closed), use_container_width=True)

    with col4:
        st.markdown(f"""
        <div style="padding-top:40px; text-align:center;">
            <div style="font-size:14px; color:white;">
                ⚠ Outstanding (>14 days)
            </div>
            <div style="font-size:26px; font-weight:800; color:#f97316;">
                {rfi_outstanding}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # FOOTER SUMMARY
    # =========================
    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:12px;
        color:#cbd5e1;
        margin-top:6px;
    ">
        TQ: {len(tq_df)} total | RFI: {len(rfi_df)} total
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
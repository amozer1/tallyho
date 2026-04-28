import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty:
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # COLUMNS
    # =========================
    status_col = next((c for c in df.columns if c.lower() == "status"), None)
    doc_col = next((c for c in df.columns if c.lower() == "doc type"), None)
    date_col = next((c for c in df.columns if c.lower() == "date sent"), None)

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns")
        return

    # =========================
    # CLEAN DATA (YOUR REAL DATA)
    # =========================
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    tq_df = df[df[doc_col] == "TQ"]
    rfi_df = df[df[doc_col] == "RFI"]

    def get_counts(sub_df):
        open_items = len(sub_df[sub_df[status_col] == "OPEN"])
        closed_items = len(sub_df[sub_df[status_col] == "CLOSED"])

        outstanding_items = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )

        return open_items, closed_items, outstanding_items

    tq_open, tq_closed, tq_outstanding = get_counts(tq_df)
    rfi_open, rfi_closed, rfi_outstanding = get_counts(rfi_df)

    # =========================
    # BRIGHT MODERN COLORS
    # =========================
    COLORS = {
        "open": "#00D9FF",
        "closed": "#00FF85",
        "outstanding": "#FF3B6B"
    }

    # =========================
    # PIE (OPEN vs CLOSED ONLY)
    # =========================
    def make_pie(title, open_count, closed_count):

        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_count, closed_count],
            hole=0.08,
            sort=False,
            marker=dict(
                colors=[COLORS["open"], COLORS["closed"]],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            textfont=dict(size=15, color="white")
        )])

        fig.update_layout(
            title=title,
            height=280,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        return fig

    # =========================
    # MAIN DASHBOARD CARD
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
        font-size:18px;
        font-weight:800;
        color:white;
        margin-bottom:12px;
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
        border-radius:14px;
        padding:12px;
        margin-bottom:12px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;font-weight:700;color:#00D9FF;'>TQ</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(
            make_pie("TQ Status", tq_open, tq_closed),
            use_container_width=True
        )

    with col2:
        st.markdown(f"""
        <div style="
            height:100%;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
            <div style="font-size:13px; color:#cbd5e1;">
                Outstanding (&gt;14 days)
            </div>
            <div style="font-size:38px; font-weight:900; color:{COLORS['outstanding']};">
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
        border-radius:14px;
        padding:12px;
        margin-bottom:8px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;font-weight:700;color:#00FF85;'>RFI</div>", unsafe_allow_html=True)

    col3, col4 = st.columns([2, 1])

    with col3:
        st.plotly_chart(
            make_pie("RFI Status", rfi_open, rfi_closed),
            use_container_width=True
        )

    with col4:
        st.markdown(f"""
        <div style="
            height:100%;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
            <div style="font-size:13px; color:#cbd5e1;">
                Outstanding (&gt;14 days)
            </div>
            <div style="font-size:38px; font-weight:900; color:{COLORS['outstanding']};">
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
        TQ Total: {len(tq_df)} | RFI Total: {len(rfi_df)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
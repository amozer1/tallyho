import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty or total == 0:
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
        st.error("Required columns missing.")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].fillna("").astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].fillna("").astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    tq_df = df[df[doc_col].str.contains("TQ", na=False)]
    rfi_df = df[df[doc_col].str.contains("RFI", na=False)]

    def get_counts(sub_df):
        closed_items = len(sub_df[sub_df[status_col].str.contains("CLOSED", na=False)])

        outstanding_items = len(
            sub_df[
                (sub_df[status_col].str.contains("OPEN", na=False)) &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )

        open_recent = len(
            sub_df[
                (sub_df[status_col].str.contains("OPEN", na=False)) &
                ((today - sub_df[date_col]).dt.days <= 14)
            ]
        )

        return open_recent, closed_items, outstanding_items

    tq_open, tq_closed, tq_outstanding = get_counts(tq_df)
    rfi_open, rfi_closed, rfi_outstanding = get_counts(rfi_df)

    overdue_total = tq_outstanding + rfi_outstanding
    overdue_pct = round((overdue_total / total) * 100, 1)

    # =========================
    # PIE CHART
    # =========================
    def make_pie(title, open_count, closed_count):
        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[max(open_count, 0.001), max(closed_count, 0.001)],
            hole=0.05,
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
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=5, r=5, t=35, b=5)
        )
        return fig

    # =========================
    # CARD START
    # =========================
    st.markdown("""
    <div style="
        background:#111827;
        border:1px solid #1f2937;
        border-radius:14px;
        padding:14px;
        margin-top:8px;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:15px;
        font-weight:700;
        color:white;
        margin-bottom:8px;
    ">
        🚨 Outstanding Tracker
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:28px;
        font-weight:800;
        color:#f97316;
        margin-bottom:4px;
    ">
        {overdue_total}
    </div>
    <div style="
        text-align:center;
        font-size:12px;
        color:#cbd5e1;
        margin-bottom:10px;
    ">
        {overdue_pct}% of total outstanding
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            make_pie("TQ", tq_open, tq_closed),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            make_pie("RFI", rfi_open, rfi_closed),
            use_container_width=True
        )

    st.markdown(f"""
    <div style="
        background:#0f172a;
        border-radius:10px;
        padding:8px;
        text-align:center;
        font-size:13px;
        color:white;
        margin-top:8px;
    ">
        ⚠ Outstanding (&gt;14 Days): 
        <span style="color:#f97316;">TQ {tq_outstanding}</span> |
        <span style="color:#f97316;">RFI {rfi_outstanding}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
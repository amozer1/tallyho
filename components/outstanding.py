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
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA
    # =========================
    tq_df = df[df[doc_col] == "TQ"]
    rfi_df = df[df[doc_col] == "RFI"]

    def get_counts(sub_df):
        closed_items = len(sub_df[sub_df[status_col] == "CLOSED"])

        outstanding_items = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )

        open_recent = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days <= 14)
            ]
        )

        return open_recent, closed_items, outstanding_items

    tq_open, tq_closed, tq_outstanding = get_counts(tq_df)
    rfi_open, rfi_closed, rfi_outstanding = get_counts(rfi_df)

    overdue_total = tq_outstanding + rfi_outstanding
    overdue_pct = round((overdue_total / total) * 100, 1)

    # =========================
    # SEVERITY
    # =========================
    if overdue_total >= 15:
        color = "#ef4444"
        status = "CRITICAL"
    elif overdue_total >= 5:
        color = "#f97316"
        status = "HIGH"
    else:
        color = "#facc15"
        status = "MEDIUM"

    # =========================
    # HEADER
    # =========================
    st.markdown(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:6px;
        text-align:center;
        font-size:12px;
        font-weight:700;
        color:{color};
        margin-bottom:8px;
    ">
        🚨 Outstanding (>14 Days) — {status}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI
    # =========================
    st.metric("Total Outstanding", overdue_total, f"{overdue_pct}% of total")

    # =========================
    # PIE CHART FUNCTION
    # =========================
    def make_pie(title, open_count, closed_count):
        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_count, closed_count],
            hole=0.05,
            sort=False,
            marker=dict(
                colors=["#38bdf8", "#22c55e"],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            insidetextorientation="horizontal",
            textfont=dict(size=16, color="white")
        )])

        fig.update_layout(
            title=title,
            height=300,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        return fig

    # =========================
    # CHARTS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            make_pie("TQ Status", tq_open, tq_closed),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            make_pie("RFI Status", rfi_open, rfi_closed),
            use_container_width=True
        )

    # =========================
    # OUTSTANDING FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        background:#111827;
        border:1px solid #1f2937;
        border-radius:10px;
        padding:8px;
        margin-top:8px;
        text-align:center;
        font-size:12px;
        color:white;
    ">
        ⚠️ <b>Outstanding (&gt;14 Days)</b><br>
        TQ: <span style="color:#f97316;">{tq_outstanding}</span> &nbsp; | &nbsp;
        RFI: <span style="color:#f97316;">{rfi_outstanding}</span>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # SUMMARY FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        font-size:11px;
        color:#cbd5e1;
        margin-top:4px;
        text-align:center;
    ">
        TQ Total: {len(tq_df)} | RFI Total: {len(rfi_df)}
    </div>
    """, unsafe_allow_html=True)
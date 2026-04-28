import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty:
        st.warning("No data available")
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
    # CLEAN DATA
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

    tq_open, tq_closed, tq_out = get_counts(tq_df)
    rfi_open, rfi_closed, rfi_out = get_counts(rfi_df)

    # =========================
    # COLOURS
    # =========================
    TQ_COLORS = {
        "open": "#A855F7",
        "closed": "#3B82F6",
        "outstanding": "#EF4444"
    }

    RFI_COLORS = {
        "open": "#14B8A6",
        "closed": "#FACC15",
        "outstanding": "#EF4444"
    }

    # =========================
    # PIE CHART (OPEN vs CLOSED ONLY)
    # =========================
    def pie(title, open_c, closed_c, colors):

        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_c, closed_c],
            hole=0.08,
            sort=False,
            marker=dict(
                colors=[colors["open"], colors["closed"]],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            textfont=dict(size=14, color="white")
        )])

        fig.update_layout(
            title=dict(text=title, font=dict(color="white", size=14)),
            height=280,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        return fig

    # =========================
    # OUTSTANDING BLOCK (CLEAN KPI)
    # =========================
    def kpi(label, value, color):
        st.markdown(f"""
        <div style="
            background:#111827;
            border:1px solid #1f2937;
            border-radius:12px;
            padding:14px;
            text-align:center;
        ">
            <div style="font-size:13px; color:#E5E7EB;">
                {label}
            </div>
            <div style="font-size:34px; font-weight:900; color:{color};">
                {value}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # DASHBOARD TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Status Dashboard")

    # =========================
    # TQ CARD
    # =========================
    with st.container():
        st.subheader("TQ")

        st.plotly_chart(
            pie(
                "Open vs Closed",
                tq_open,
                tq_closed,
                TQ_COLORS
            ),
            use_container_width=True
        )

        kpi("Outstanding (>14 days)", tq_out, TQ_COLORS["outstanding"])

    st.divider()

    # =========================
    # RFI CARD
    # =========================
    with st.container():
        st.subheader("RFI")

        st.plotly_chart(
            pie(
                "Open vs Closed",
                rfi_open,
                rfi_closed,
                RFI_COLORS
            ),
            use_container_width=True
        )

        kpi("Outstanding (>14 days)", rfi_out, RFI_COLORS["outstanding"])

    # =========================
    # FOOTER
    # =========================
    st.markdown(
        f"**Totals → TQ:** {len(tq_df)} | **RFI:** {len(rfi_df)}"
    )
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df):

    if df is None or df.empty:
        st.warning("No data available")
        return

    df = df.copy()
    df.columns = df.columns.str.strip()

    # =========================
    # REQUIRED COLUMNS
    # =========================
    status_col = next((c for c in df.columns if c.lower() == "status"), None)
    doc_col = next((c for c in df.columns if c.lower() == "doc type"), None)
    date_col = next((c for c in df.columns if c.lower() == "date sent"), None)

    if not status_col or not doc_col or not date_col:
        st.error("Missing required columns: Status / Doc Type / Date Sent")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df[status_col] = df[status_col].astype(str).str.strip().str.upper()
    df[doc_col] = df[doc_col].astype(str).str.strip().str.upper()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT
    # =========================
    rfi_df = df[df[doc_col] == "RFI"]
    tq_df = df[df[doc_col] == "TQ"]

    # =========================
    # COUNTS
    # =========================
    def get_counts(sub_df):
        open_items = len(sub_df[sub_df[status_col] == "OPEN"])
        closed_items = len(sub_df[sub_df[status_col] == "CLOSED"])

        outstanding_items = len(
            sub_df[
                (sub_df[status_col] == "OPEN") &
                ((today - sub_df[date_col]).dt.days > 14)
            ]
        )

        return open_items, outstanding_items, closed_items

    rfi_open, rfi_out, rfi_closed = get_counts(rfi_df)
    tq_open, tq_out, tq_closed = get_counts(tq_df)

    # =========================
    # COLOURS
    # =========================
    COLORS = {
        "open": "#EF4444",
        "out": "#F59E0B",
        "closed": "#22C55E"
    }

    # =========================
    # PIE BUILDER (SOLID)
    # =========================
    def build_pie(title, open_c, out_c, closed_c):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[open_c, out_c, closed_c],
            hole=0,
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="#0f172a", width=2)
            ),
            textinfo="label+percent",
            textposition="inside",
            sort=False
        ))

        fig.update_layout(
            title=dict(text=title, x=0.5),
            height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        return fig

    # =========================
    # LAYOUT (SIDE BY SIDE)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("RFI Status")
        st.plotly_chart(
            build_pie("RFI", rfi_open, rfi_out, rfi_closed),
            use_container_width=True
        )

    with col2:
        st.subheader("TQ Status")
        st.plotly_chart(
            build_pie("TQ", tq_open, tq_out, tq_closed),
            use_container_width=True
        )
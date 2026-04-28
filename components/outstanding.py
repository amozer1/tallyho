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
    # COLOURS (ONLY CHANGE MADE HERE)
    # =========================
    TQ = {
        "open": "#3B82F6",        # blue
        "closed": "#22C55E",      # green
        "out": "#EF4444"          # red
    }

    RFI = {
        "open": "#A78BFA",        # light purple
        "closed": "#6D28D9",      # deep purple
        "out": "#EF4444"          # red
    }

    # =========================
    # CARD BUILDER
    # =========================
    def card(title, open_c, closed_c, out_c, colors):

        fig = go.Figure()

        # =========================
        # PIE
        # =========================
        fig.add_trace(go.Pie(
            labels=["Open", "Closed", "Outstanding"],
            values=[open_c, closed_c, out_c],

            hole=0.12,

            marker=dict(
                colors=[colors["open"], colors["closed"], colors["out"]],
                line=dict(color="#111827", width=2)
            ),

            textinfo="label+value",
            textposition="inside",
            insidetextorientation="radial",
            textfont=dict(color="white", size=11)
        ))

        # =========================
        # TITLE
        # =========================
        fig.add_annotation(
            text=f"<b>{title} Information</b>",
            x=0.5, y=1.08,
            showarrow=False,
            font=dict(size=16, color="white")
        )

        # =========================
        # OPEN / CLOSED TEXT
        # =========================
        fig.add_annotation(
            text=f"Open: {open_c} | Closed: {closed_c}",
            x=0.5, y=-0.06,
            showarrow=False,
            font=dict(size=11, color="#cbd5e1")
        )

        # =========================
        # OUTSTANDING
        # =========================
        fig.add_annotation(
            text=f"Outstanding (>14 days): {out_c}",
            x=0.5, y=-0.16,
            showarrow=False,
            font=dict(size=12, color=colors["out"])
        )

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(
            height=290,
            margin=dict(l=10, r=10, t=35, b=45),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )

        return fig

    # =========================
    # OUTPUT
    # =========================
    st.plotly_chart(card("TQ", tq_open, tq_closed, tq_out, TQ), use_container_width=True)
    st.plotly_chart(card("RFI", rfi_open, rfi_closed, rfi_out, RFI), use_container_width=True)
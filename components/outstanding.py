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
    # THEMES
    # =========================
    TQ = {"open": "#A855F7", "closed": "#3B82F6", "out": "#EF4444"}
    RFI = {"open": "#14B8A6", "closed": "#FACC15", "out": "#EF4444"}

    # =========================
    # CARD BUILDER
    # =========================
    def card(title, open_c, closed_c, out_c, colors):

        fig = go.Figure()

        # =========================
        # PIE (REMOVE ZEROS ONLY)
        # =========================
        labels = []
        values = []
        pie_colors = []

        if open_c >= 1:
            labels.append("Open")
            values.append(open_c)
            pie_colors.append(colors["open"])

        if closed_c >= 1:
            labels.append("Closed")
            values.append(closed_c)
            pie_colors.append(colors["closed"])

        if values:
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                hole=0.12,

                marker=dict(
                    colors=pie_colors,
                    line=dict(color="#0f172a", width=2)
                ),

                # 🔥 FORCE LABELS INSIDE
                textinfo="label+value",
                textposition="inside",
                insidetextorientation="radial",
                textfont=dict(color="white", size=14),
                automargin=False
            ))
        else:
            fig.add_annotation(
                text="No Open/Closed Items",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="white")
            )

        # =========================
        # TITLE
        # =========================
        fig.add_annotation(
            text=f"<b>{title}</b>",
            x=0.5, y=1.15,
            showarrow=False,
            font=dict(size=18, color="white")
        )

        # =========================
        # OPEN / CLOSED TEXT
        # =========================
        fig.add_annotation(
            text=f"Open: {open_c}   |   Closed: {closed_c}",
            x=0.5, y=-0.10,
            showarrow=False,
            font=dict(size=12, color="#cbd5e1")
        )

        # =========================
        # OUTSTANDING
        # =========================
        fig.add_annotation(
            text=f"Outstanding (>14 days): {out_c}",
            x=0.5, y=-0.22,
            showarrow=False,
            font=dict(size=14, color=colors["out"])
        )

        # =========================
        # LAYOUT FIX (IMPORTANT)
        # =========================
        fig.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=50, b=70),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,

            # 🔥 prevents label escaping
            uniformtext_minsize=12,
            uniformtext_mode="hide"
        )

        return fig

    # =========================
    # DASHBOARD
    # =========================
    st.markdown("### 📊 TQ & RFI Status Dashboard")

    st.plotly_chart(card("TQ", tq_open, tq_closed, tq_out, TQ), use_container_width=True)
    st.plotly_chart(card("RFI", rfi_open, rfi_closed, rfi_out, RFI), use_container_width=True)
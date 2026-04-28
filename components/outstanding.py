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
    # PIE (FIXED TEXT INSIDE SLICES)
    # =========================
    def pie(open_c, closed_c, colors):

        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_c, closed_c],

            sort=False,
            hole=0.12,
            pull=0,

            marker=dict(
                colors=[colors["open"], colors["closed"]],
                line=dict(color="#0f172a", width=2)
            ),

            # 🔥 KEY FIX: text fully inside slice
            textinfo="label+value",
            textposition="inside",
            insidetextorientation="radial",
            texttemplate="%{label}<br>%{value}",
            textfont=dict(color="white", size=14)
        )])

        fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            automargin=True
        )

        return fig

    # =========================
    # CARD BUILDER
    # =========================
    def card(title, open_c, closed_c, out_c, colors):

        st.markdown(f"### {title}")

        st.plotly_chart(
            pie(open_c, closed_c, colors),
            use_container_width=True
        )

        st.markdown(
            f"""
            **Outstanding (>14 days):**  
            <span style="color:{colors['out']}; font-size:18px; font-weight:700;">
            {out_c}
            </span>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # DASHBOARD
    # =========================
    st.markdown("### 📊 TQ & RFI Status Dashboard")

    card("TQ", tq_open, tq_closed, tq_out, TQ)
    card("RFI", rfi_open, rfi_closed, rfi_out, RFI)
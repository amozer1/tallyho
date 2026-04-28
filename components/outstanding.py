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
    # COLUMN DETECTION
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
    # COLORS (CLEAR + DISTINCT)
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
    # PIE
    # =========================
    def pie(title, open_c, closed_c, colors):
        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_c, closed_c],
            hole=0.12,
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
            height=260,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        return fig

    # =========================
    # CARD WRAPPER (TRUE STRUCTURE FIX)
    # =========================
    def render_card(title, open_c, closed_c, out_c, colors):

        st.markdown(
            f"""
            <div style="
                background:#111827;
                border:1px solid #1f2937;
                border-radius:14px;
                padding:14px;
                margin-bottom:14px;
            ">
            <div style="
                text-align:center;
                font-size:16px;
                font-weight:800;
                color:{colors['open']};
                margin-bottom:8px;
            ">
                {title}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            pie("Open vs Closed", open_c, closed_c, colors),
            use_container_width=True
        )

        st.markdown(
            f"""
            <div style="
                margin-top:10px;
                padding:12px;
                border-radius:10px;
                background:#0f172a;
                border:1px solid #1f2937;
                text-align:center;
            ">
                <div style="color:#cbd5e1; font-size:13px;">
                    Outstanding (>14 days)
                </div>
                <div style="font-size:34px; font-weight:900; color:{colors['outstanding']};">
                    {out_c}
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 TQ & RFI Status Dashboard")

    # =========================
    # RENDER CARDS (STACKED CLEANLY)
    # =========================
    render_card("TQ", tq_open, tq_closed, tq_out, TQ_COLORS)
    render_card("RFI", rfi_open, rfi_closed, rfi_out, RFI_COLORS)

    # =========================
    # FOOTER
    # =========================
    st.markdown(
        f"**Totals → TQ:** {len(tq_df)} | **RFI:** {len(rfi_df)}"
    )
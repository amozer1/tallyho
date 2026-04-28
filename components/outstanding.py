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
    # THEMES (DIFFERENT PER CARD)
    # =========================
    TQ_COLORS = {
        "open": "#A855F7",       # purple
        "closed": "#3B82F6",     # blue
        "outstanding": "#EF4444" # red
    }

    RFI_COLORS = {
        "open": "#14B8A6",       # teal
        "closed": "#FACC15",     # yellow
        "outstanding": "#EF4444" # red
    }

    # =========================
    PIE FUNCTION
    # =========================
    def pie(title, open_c, closed_c, colors):
        fig = go.Figure(data=[go.Pie(
            labels=["Open", "Closed"],
            values=[open_c, closed_c],
            hole=0.08,
            marker=dict(
                colors=[colors["open"], colors["closed"]],
                line=dict(color="#111827", width=2)
            ),
            textinfo="label+value",
            textposition="inside",
            textfont=dict(size=14, color="white")
        )])

        fig.update_layout(
            title=dict(text=title, font=dict(color="white", size=14)),
            height=250,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False,
            margin=dict(l=10, r=10, t=35, b=10)
        )
        return fig

    # =========================
    OUTSTANDING BLOCK (CLEAR TEXT INSIDE CARD)
    # =========================
    def outstanding_block(label, value, color):
        return f"""
        <div style="
            background:#111827;
            border:1px solid #1f2937;
            border-radius:12px;
            padding:12px;
            text-align:center;
            margin-top:10px;
        ">
            <div style="
                font-size:13px;
                color:#E5E7EB;
                font-weight:500;
            ">
                {label}
            </div>

            <div style="
                font-size:34px;
                font-weight:900;
                color:{color};
                margin-top:4px;
            ">
                {value}
            </div>
        </div>
        """

    # =========================
    DASHBOARD WRAPPER
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
        margin-bottom:14px;
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

    st.markdown("""
    <div style="
        text-align:center;
        font-weight:700;
        color:#A855F7;
        margin-bottom:6px;
    ">
        TQ
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        pie("TQ: Open vs Closed", tq_open, tq_closed, TQ_COLORS),
        use_container_width=True
    )

    st.markdown(
        outstanding_block("Outstanding (>14 days)", tq_out, TQ_COLORS["outstanding"]),
        unsafe_allow_html=True
    )

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

    st.markdown("""
    <div style="
        text-align:center;
        font-weight:700;
        color:#14B8A6;
        margin-bottom:6px;
    ">
        RFI
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        pie("RFI: Open vs Closed", rfi_open, rfi_closed, RFI_COLORS),
        use_container_width=True
    )

    st.markdown(
        outstanding_block("Outstanding (>14 days)", rfi_out, RFI_COLORS["outstanding"]),
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # FOOTER
    # =========================
    st.markdown(f"""
    <div style="
        text-align:center;
        font-size:12px;
        color:#CBD5E1;
        margin-top:6px;
    ">
        TQ Total: {len(tq_df)} | RFI Total: {len(rfi_df)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
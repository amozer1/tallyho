import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_outstanding_line(df, total):

    if df is None or df.empty:
        st.warning("No data available")
        return

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    required = ["doc type", "status", "date sent"]
    for col in required:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return

    df["doc type"] = df["doc type"].astype(str).str.upper().str.strip()
    df["status"] = df["status"].astype(str).str.upper().str.strip()
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # FILTER TOGGLE
    # =========================
    doc_view = st.radio(
        "",
        ["RFIs", "TQs", "Both"],
        horizontal=True
    )

    # =========================
    # COUNTS
    # =========================
    def get_counts(sub_df):
        open_count = len(sub_df[sub_df["status"] == "OPEN"])
        closed_count = len(sub_df[sub_df["status"] == "CLOSED"])
        outstanding_count = len(
            sub_df[
                (sub_df["status"] == "OPEN") &
                ((today - sub_df["date sent"]).dt.days > 14)
            ]
        )
        return open_count, outstanding_count, closed_count

    rfi_df = df[df["doc type"] == "RFI"]
    tq_df = df[df["doc type"] == "TQ"]

    rfi_open, rfi_out, rfi_closed = get_counts(rfi_df)
    tq_open, tq_out, tq_closed = get_counts(tq_df)

    # KPI totals
    if doc_view == "RFIs":
        k_open, k_out, k_closed = rfi_open, rfi_out, rfi_closed
    elif doc_view == "TQs":
        k_open, k_out, k_closed = tq_open, tq_out, tq_closed
    else:
        k_open = rfi_open + tq_open
        k_out = rfi_out + tq_out
        k_closed = rfi_closed + tq_closed

    # =========================
    # KPI CARDS
    # =========================
    c1, c2, c3 = st.columns(3)

    def card(col, title, value, color):
        with col:
            st.markdown(f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:18px;
                text-align:center;
                border:1px solid #e5e7eb;">
                <h3 style="margin:0;color:{color};">{title}</h3>
                <h1 style="margin:0;color:#111827;">{value}</h1>
            </div>
            """, unsafe_allow_html=True)

    card(c1, "Open", k_open, "#EF4444")
    card(c2, "Outstanding", k_out, "#EAB308")
    card(c3, "Closed", k_closed, "#22C55E")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # PIE CHART
    # =========================
    def make_pie(title, open_v, out_v, closed_v):
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[open_v, out_v, closed_v],
            hole=0.45,
            marker=dict(
                colors=["#EF4444", "#F59E0B", "#16A34A"],
                line=dict(color="white", width=2)
            ),
            textinfo="percent",
            textfont=dict(size=20, color="white"),
            sort=False
        ))

        fig.update_layout(
            title=f"<b>{title}</b>",
            height=320,
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=True,
            legend=dict(
                orientation="v",
                x=0,
                y=0.8,
                font=dict(size=16)
            )
        )

        return fig

    # =========================
    # MIDDLE ROW
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        if doc_view in ["RFIs", "Both"]:
            st.plotly_chart(
                make_pie("RFI", rfi_open, rfi_out, rfi_closed),
                use_container_width=True,
                key="rfi_pie"
            )

    with col2:
        if doc_view in ["TQs", "Both"]:
            st.plotly_chart(
                make_pie("TQ", tq_open, tq_out, tq_closed),
                use_container_width=True,
                key="tq_pie"
            )

    # =========================
    # NOTES SECTION
    # =========================
    n1, n2 = st.columns(2)

    with n1:
        st.markdown("""
        <div style="
            background:white;
            border-radius:12px;
            padding:20px;
            border:1px solid #e5e7eb;
            min-height:260px;">
            <h2>RFI</h2>
            <hr>
            <b>Key Issues</b><br>
            Outstanding RFIs mainly relate to design coordination and interface queries.<br><br>

            <b>Actions / Owners</b><br>
            Consultant review underway, contractor consolidating responses.<br><br>

            <b>Outlook / Risk</b><br>
            Likely to reduce next week if revised drawings are issued.
        </div>
        """, unsafe_allow_html=True)

    with n2:
        st.markdown("""
        <div style="
            background:white;
            border-radius:12px;
            padding:20px;
            border:1px solid #e5e7eb;
            min-height:260px;">
            <h2>TQ</h2>
            <hr>
            <b>Key Issues</b><br>
            TQs driven by façade details and procurement clarifications.<br><br>

            <b>Actions / Owners</b><br>
            Design manager reviewing batches this week.<br><br>

            <b>Outlook / Risk</b><br>
            Stable unless new package release creates additional queries.
        </div>
        """, unsafe_allow_html=True)
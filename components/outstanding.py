import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import re


def render_outstanding_line(df, total):

    if df is None or df.empty:
        st.warning("No data available")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    required = [
        "project id", "doc type", "status",
        "date sent", "required date",
        "subject", "sender", "recipient"
    ]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    df["doc type"] = df["doc type"].astype(str).str.upper().str.strip()
    df["status"] = df["status"].astype(str).str.upper().str.strip()
    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["required date"] = pd.to_datetime(df["required date"], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SINGLE BUILDING CONTEXT
    # =========================
    project_name = df["project id"].dropna().iloc[0]

    st.markdown(f"""
        <h1 style='text-align:center; margin-bottom:10px;'>
            {project_name} – RFI / TQ Overview
        </h1>
    """, unsafe_allow_html=True)

    # =========================
    # RFIs / TQs SELECTOR
    # =========================
    doc_view = st.radio(
        "",
        ["RFIs", "TQs", "Both"],
        horizontal=True
    )

    # =========================
    # COUNTS LOGIC
    # =========================
    def get_counts(sub_df):
        open_count = len(sub_df[sub_df["status"] == "OPEN"])
        closed_count = len(sub_df[sub_df["status"] == "CLOSED"])
        outstanding_count = len(
            sub_df[
                (sub_df["status"] == "OPEN") &
                (sub_df["required date"] < today)
            ]
        )
        return open_count, outstanding_count, closed_count

    rfi_df = df[df["doc type"] == "RFI"]
    tq_df = df[df["doc type"] == "TQ"]

    rfi_open, rfi_out, rfi_closed = get_counts(rfi_df)
    tq_open, tq_out, tq_closed = get_counts(tq_df)

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
    # PIE CHARTS
    # =========================
    def make_pie(title, open_v, out_v, closed_v):
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[open_v, out_v, closed_v],
            hole=0,
            marker=dict(
                colors=["#EF4444", "#EAB308", "#22C55E"],
                line=dict(color="white", width=2)
            ),
            textinfo="percent",
            textfont=dict(size=18, color="white"),
            sort=False
        ))

        fig.update_layout(
            title=f"<b>{title}</b>",
            height=330,
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=True,
            legend=dict(
                orientation="v",
                x=0,
                y=0.85
            )
        )

        return fig

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
    # NOTES LOGIC
    # =========================
    def generate_notes(sub_df):
        open_df = sub_df[sub_df["status"] == "OPEN"]

        # KEY ISSUES
        words = []
        for s in open_df["subject"].dropna():
            words += re.findall(r"\b[A-Za-z]{4,}\b", s.lower())

        stopwords = {
            "mae", "rfi", "tq", "confirm",
            "outline", "design", "solution",
            "existing"
        }

        words = [w for w in words if w not in stopwords]
        common_words = [w[0] for w in Counter(words).most_common(4)]
        key_issues = ", ".join(common_words).title() if common_words else "No clear trend"

        # ACTIONS / OWNERS
        owner = (
            open_df["recipient"].mode().iloc[0]
            if not open_df["recipient"].mode().empty
            else "Unassigned"
        )

        # OUTLOOK / RISK
        overdue = len(open_df[open_df["required date"] < today])

        if overdue > 10:
            outlook = "High overdue risk / likely increase"
        elif overdue > 5:
            outlook = "Moderate risk / monitor closely"
        else:
            outlook = "Stable / manageable"

        return key_issues, owner, outlook

    rfi_issues, rfi_owner, rfi_outlook = generate_notes(rfi_df)
    tq_issues, tq_owner, tq_outlook = generate_notes(tq_df)

    # =========================
    # BOTTOM STRUCTURED NOTES
    # =========================
    n1, n2 = st.columns(2)

    def note_card(col, title, issues, owner, outlook):
        with col:
            st.markdown(f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:20px;
                border:1px solid #e5e7eb;
                min-height:260px;">
                <h2>{title}</h2>
                <hr>

                <b>Key Issues</b><br>
                {issues}<br><br>

                <b>Actions / Owners</b><br>
                {owner}<br><br>

                <b>Outlook / Risk</b><br>
                {outlook}
            </div>
            """, unsafe_allow_html=True)

    note_card(n1, "RFI Notes", rfi_issues, rfi_owner, rfi_outlook)
    note_card(n2, "TQ Notes", tq_issues, tq_owner, tq_outlook)
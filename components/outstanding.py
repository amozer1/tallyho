import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_outstanding_line(df, total=None):

    if df is None or df.empty:
        st.warning("No data available")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    status_col = "status"
    doc_col = "doc type"
    date_col = "date sent"

    df[status_col] = df[status_col].astype(str).str.upper().str.strip()
    df[doc_col] = df[doc_col].astype(str).str.upper().str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    today = pd.Timestamp.today()

    # =========================
    # SPLIT DATA
    # =========================
    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    def calc(sub):
        open_ = len(sub[sub[status_col] == "OPEN"])
        closed_ = len(sub[sub[status_col] == "CLOSED"])
        outstanding_ = len(
            sub[
                (sub[status_col] == "OPEN") &
                ((today - sub[date_col]).dt.days > 14)
            ]
        )
        return open_, outstanding_, closed_

    rfi_open, rfi_out, rfi_closed = calc(rfi)
    tq_open, tq_out, tq_closed = calc(tq)

    # =========================
    # AI NOTES (REAL DATA)
    # =========================
    def generate_notes(df):

        overdue = df[
            (df[status_col] == "OPEN") &
            ((today - df[date_col]).dt.days > 14)
        ]

        overdue_count = len(overdue)

        # THEME DETECTION FROM YOUR SUBJECTS
        themes = {
            "rising main": "rising mains",
            "screening chamber": "screening chamber interfaces",
            "mh": "manhole design",
            "manhole": "manhole design",
            "diversion": "diversion works",
            "existing": "existing asset coordination"
        }

        theme_hits = {}

        if "subject" in df.columns:
            subjects = df["subject"].dropna().astype(str).str.lower()

            for key, label in themes.items():
                count = subjects.str.contains(key).sum()
                if count > 0:
                    theme_hits[label] = count

        top_drivers = sorted(theme_hits, key=theme_hits.get, reverse=True)[:3]

        note = ""

        if overdue_count > 0:
            note += f"High volume of overdue queries ({overdue_count} items)"

        if top_drivers:
            note += f", primarily related to {', '.join(top_drivers)}"

        note += "."

        return note

    notes_text = generate_notes(df)

    # =========================
    # COLORS
    # =========================
    COLORS = {
        "open": "#ef4444",
        "out": "#f59e0b",
        "closed": "#22c55e"
    }

    # =========================
    # HEADER
    # =========================
    st.markdown(
        "<h1 style='text-align:center;'>Building A – RFI / TQ Overview</h1>",
        unsafe_allow_html=True
    )

    # =========================
    # TOGGLE
    # =========================
    _, toggle_col, _ = st.columns([3, 2, 3])
    with toggle_col:
        view = st.radio("", ["RFI", "TQ"], horizontal=True)

    if view == "RFI":
        open_, out_, closed_ = rfi_open, rfi_out, rfi_closed
    else:
        open_, out_, closed_ = tq_open, tq_out, tq_closed

    # =========================
    # KPI CARDS
    # =========================
    def kpi_card(title, value):
        st.markdown(f"""
        <div style="
            padding:16px;
            border-radius:10px;
            border:1px solid #e5e7eb;
            background:white;
            text-align:center;
        ">
            <h4 style="margin-bottom:5px;">{title}</h4>
            <h1 style="margin:0;">{value}</h1>
        </div>
        """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)

    with k1:
        kpi_card("Open", open_)
    with k2:
        kpi_card("Outstanding", out_)
    with k3:
        kpi_card("Closed", closed_)

    # =========================
    # PIE FUNCTION
    # =========================
    def pie(o, out, c):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open", "Outstanding", "Closed"],
            values=[o, out, c],
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["closed"]],
                line=dict(color="white", width=2)
            ),
            textinfo="percent",
            sort=False
        ))

        fig.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )

        return fig

    # =========================
    # CARD WRAPPER
    # =========================
    def chart_card(title, fig, key):
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.plotly_chart(fig, use_container_width=True, key=key)

    # =========================
    # PIE ROW
    # =========================
    c1, c2 = st.columns(2, gap="large")

    with c1:
        chart_card("RFI", pie(rfi_open, rfi_out, rfi_closed), "rfi_pie")

    with c2:
        chart_card("TQ", pie(tq_open, tq_out, tq_closed), "tq_pie")

    # =========================
    # BOTTOM CARDS
    # =========================
    b1, b2 = st.columns(2)

    with b1:
        with st.container(border=True):
            st.markdown("### Key Issues")
            st.write(
                f"{rfi_out + tq_out} items are overdue across RFIs and TQs, "
                "requiring immediate coordination focus."
            )

    with b2:
        with st.container(border=True):
            st.markdown("### Notes")
            st.write(notes_text)
            st.write(
                "**Actions:** Immediate focus required on overdue items and key coordination areas."
            )
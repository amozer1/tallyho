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

    rfi = df[df[doc_col] == "RFI"]
    tq = df[df[doc_col] == "TQ"]

    # =========================
    # SLA LOGIC (UPDATED)
    # =========================
    def calc(sub):

        open_0_7 = len(
            sub[
                (sub[status_col] == "OPEN") &
                (sub[date_col].notna()) &
                ((today - sub[date_col]).dt.days <= 7)
            ]
        )

        outstanding_7_14 = len(
            sub[
                (sub[status_col] == "OPEN") &
                (sub[date_col].notna()) &
                ((today - sub[date_col]).dt.days > 7) &
                ((today - sub[date_col]).dt.days <= 14)
            ]
        )

        overdue_14_plus = len(
            sub[
                (sub[status_col] == "OPEN") &
                (sub[date_col].notna()) &
                ((today - sub[date_col]).dt.days > 14)
            ]
        )

        return open_0_7, outstanding_7_14, overdue_14_plus

    rfi_open, rfi_out, rfi_overdue = calc(rfi)
    tq_open, tq_out, tq_overdue = calc(tq)

    COLORS = {
        "open": "#22c55e",        # green
        "out": "#f59e0b",        # amber
        "overdue": "#ef4444"     # red
    }

    # =========================
    # PIE CHART
    # =========================
    def pie(o, out, od):

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=["Open (0-7d)", "Outstanding (7-14d)", "Overdue (14d+)"],
            values=[o, out, od],
            textinfo="label+value",
            marker=dict(
                colors=[COLORS["open"], COLORS["out"], COLORS["overdue"]],
                line=dict(color="white", width=2)
            ),
            sort=False
        ))

        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=12)
        )

        return fig

    # =========================
    # CARD
    # =========================
    def card(title, o, out, od):

        st.markdown(f"### {title} SLA Overview")

        st.markdown(
            f"""
            🟢 **Open (0–7d):** {o}  
            🟡 **Outstanding (7–14d):** {out}  
            🔴 **Overdue (14+d):** {od}
            """
        )

        st.plotly_chart(
            pie(o, out, od),
            use_container_width=True
        )

        st.divider()

    # =========================
    # LAYOUT
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        card("RFI", rfi_open, rfi_out, rfi_overdue)

    with col2:
        card("TQ", tq_open, tq_out, tq_overdue)
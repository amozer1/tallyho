import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_venn_overview(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    df.columns = [c.strip().lower() for c in df.columns]

    # =========================
    # REQUIRED FIELDS
    # =========================
    required = ["doc type", "required date", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # PARSE DATES
    # =========================
    df["required date"] = pd.to_datetime(df["required date"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    # =========================
    # CLASSIFICATION
    # =========================

    # SLA rule: 7 days buffer
    df["sla_due"] = df["required date"] + pd.Timedelta(days=7)

    df["status_group"] = "SLA Compliant"

    # Overdue condition
    df.loc[
        (df["reply date"].isna()) |
        (df["reply date"] > df["sla_due"]),
        "status_group"
    ] = "Overdue"

    # Split TQ / RFI inside categories
    df["type_group"] = df["doc type"].str.upper()

    # =========================
    # COUNTS (NO DUPLICATION)
    # =========================
    tq_total = len(df[df["doc type"] == "tq"])
    rfi_total = len(df[df["doc type"] == "rfi"])

    overdue = len(df[df["status_group"] == "Overdue"])
    sla_ok = len(df[df["status_group"] == "SLA Compliant"])

    # =========================
    # TITLE
    # =========================
    st.markdown("## Communication Health Overview")

    # =========================
    # DONUT CHART (CLEAN VISUAL)
    # =========================
    fig = go.Figure(data=[go.Pie(
        labels=["TQ / RFI Total", "Overdue (>7 days)", "SLA Compliant"],
        values=[tq_total + rfi_total, overdue, sla_ok],
        hole=0.65,
        marker=dict(colors=["#4da3ff", "#ff4d4d", "#22c55e"])
    )])

    fig.update_layout(
        showlegend=True,
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # SUMMARY METRICS (CLEAR, NO DUPLICATION)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total TQs", tq_total)

    with col2:
        st.metric("Total RFIs", rfi_total)

    with col3:
        st.metric("Overdue Items", overdue)

    # =========================
    # INSIGHT
    # =========================
    st.markdown("---")

    st.markdown(f"""
### Insight Summary
- SLA Compliance Rate: **{round((sla_ok / len(df)) * 100, 1)}%**
- Overdue Rate: **{round((overdue / len(df)) * 100, 1)}%**

> This view represents overall communication health across TQ and RFI workflows without duplication or double counting.
""")
import streamlit as st


def render_overdue_alert(overdue, total, tq_not, rfi_not, tq_not_pct, rfi_not_pct):
    """
    Standalone overdue KPI alert component
    """

    # =========================
    # SAFETY CHECK
    # =========================
    if total == 0:
        return

    overdue_pct = round((overdue / total) * 100, 1)

    # =========================
    # SEVERITY LOGIC
    # =========================
    if overdue_pct < 20:
        severity_color = "#22c55e"  # green
        severity_label = "LOW"
    elif overdue_pct < 40:
        severity_color = "#f59e0b"  # amber
        severity_label = "MEDIUM"
    else:
        severity_color = "#ef4444"  # red
        severity_label = "HIGH"

    # =========================
    # ALERT UI
    # =========================
    st.markdown(
        f"""
        <div style="
            padding: 12px 14px;
            border-radius: 10px;
            background: rgba(0,0,0,0.25);
            border: 1px solid {severity_color};
            margin-bottom: 12px;
            max-width: 540px;
        ">
            <div style="color:{severity_color}; font-weight:900; font-size:14px;">
                ⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)
                <span style="float:right;">{severity_label} RISK</span>
            </div>

            <div style="margin-top:6px; color:white; font-size:13px;">
                🔵 TQ: {tq_not} ({tq_not_pct}%)<br>
                🟢 RFI: {rfi_not} ({rfi_not_pct}%)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# OPTIONAL DRILLDOWN
# =========================
def render_overdue_button(df):
    if st.button("🔍 View Overdue Items"):
        st.dataframe(
            df[(df["reply date"].isna()) & (df["age"] > 7)]
        )
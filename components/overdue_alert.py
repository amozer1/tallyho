import streamlit as st


def render_overdue_alert(overdue, total, tq_not, rfi_not,
                         tq_not_pct, rfi_not_pct):

    # =========================
    # SAFETY CHECK
    # =========================
    if total is None or total == 0:
        st.info("No data available for overdue analysis.")
        return

    overdue = overdue or 0
    tq_not = tq_not or 0
    rfi_not = rfi_not or 0
    tq_not_pct = tq_not_pct or 0
    rfi_not_pct = rfi_not_pct or 0

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
    # ALERT UI (STREAMLIT SAFE HTML)
    # =========================
    st.markdown(
        f"""
        <div style="
            padding: 14px 16px;
            border-radius: 10px;
            background: rgba(0,0,0,0.30);
            border: 1px solid {severity_color};
            margin-bottom: 14px;
        ">
            <div style="color:{severity_color}; font-weight:900; font-size:15px;">
                ⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)
                <span style="float:right;">{severity_label} RISK</span>
            </div>

            <div style="margin-top:8px; color:white; font-size:13px; line-height:1.6;">
                🔵 TQ: {tq_not} ({tq_not_pct}%)<br>
                🟢 RFI: {rfi_not} ({rfi_not_pct}%)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# OPTIONAL DRILLDOWN TABLE
# =========================
def render_overdue_button(df):

    if df is None or df.empty:
        return

    if st.button("🔍 View Overdue Items"):

        filtered = df[(df["reply date"].isna()) & (df["age"] > 7)]

        st.markdown("### 🔴 Overdue Records (>7 Days)")
        st.dataframe(filtered, use_container_width=True)
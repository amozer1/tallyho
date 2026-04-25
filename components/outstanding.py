import streamlit as st


def render_outstanding(overdue, total, tq_not, rfi_not, tq_total, rfi_total):

    if total == 0:
        st.warning("No data available")
        return

    overdue_pct = round((overdue / total) * 100, 1)

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0

    # =========================
    # SIMPLE RISK LEVEL
    # =========================
    if overdue_pct >= 40:
        st.error(f"⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%) — HIGH RISK")
    elif overdue_pct >= 20:
        st.warning(f"⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%) — MEDIUM RISK")
    else:
        st.success(f"⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%) — LOW RISK")

    # =========================
    # BREAKDOWN
    # =========================
    st.markdown(f"""
🔵 **TQ Not Responded:** {tq_not} ({tq_not_pct}%)

🟢 **RFI Not Responded:** {rfi_not} ({rfi_not_pct}%)
""")
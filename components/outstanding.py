import streamlit as st


def render_outstanding_line(overdue, total, tq_not, rfi_not):

    # =========================
    # SAFETY CHECK
    # =========================
    if total is None or total == 0:
        st.warning("No data available")
        return

    # =========================
    # REAL DATA PERCENTAGES
    # =========================
    overdue_pct = round((overdue / total) * 100, 1)

    tq_not_pct = round((tq_not / total) * 100, 1)
    rfi_not_pct = round((rfi_not / total) * 100, 1)

    # =========================
    # MAIN OUTSTANDING ALERT
    # =========================
    st.markdown(f"""
### ⚠ Outstanding > 7 Days: {overdue} ({overdue_pct}%)

🔵 **TQ Not Responded:** {tq_not} ({tq_not_pct}%)  
🟢 **RFI Not Responded:** {rfi_not} ({rfi_not_pct}%)
""")
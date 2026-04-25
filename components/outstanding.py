import streamlit as st


def render_outstanding_line(df, total):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or total == 0:
        st.warning("No data available")
        return

    # =========================
    # FILTER: OVERDUE (>7 DAYS + NOT REPLIED)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue = len(overdue_df)
    overdue_pct = round((overdue / total) * 100, 1)

    # =========================
    # BREAKDOWN
    # =========================
    overdue_tq = len(overdue_df[overdue_df["doc type"].str.lower() == "tq"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"].str.lower() == "rfi"])

    # =========================
    # UI
    # =========================
    st.markdown(f"""
### ⚠ Overdue (> 7 Days)

🔴 Overdue = **{overdue}** ({overdue_pct}%)

➡ TQ overdue: **{overdue_tq}**  
➡ RFI overdue: **{overdue_rfi}**
""")